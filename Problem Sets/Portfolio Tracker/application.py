import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # greet user by their username
    welcome_user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    # generate portfolio of user
    # group by symbol, sum up the number of shares of each symbol
    holdings = db.execute(
        "SELECT symbol, name, price, SUM(shares) as shares, total FROM holdings WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    # retrieve remaining cash amount from user's profile
    remaining_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    # calculate amount user has in stocks (live price)
    total_stock_value = 0
    for holding in holdings:

        # look up is a function that will store everything about the particular stock
        # when buying, sufficient to input the symbol and quantity into holdings database, live data will be updated and presented in home page.
        stock = lookup(holding["symbol"])
        # as defined in helpers.py:
        # companyName: name
        # latestPrice: price
        holding["name"] = stock["Name"]
        holding["price"] = stock["Price"]
        holding["total"] = holding["price"] * holding["shares"]

        total_stock_value = total_stock_value + holding["total"]

    # calculate total amount user has (remaining cash + stock)
    total_value = total_stock_value + remaining_cash[0]["cash"]

    # convert to usd in template
    return render_template("index.html", welcome_user=welcome_user[0]["username"], holdings=holdings, remaining_cash=remaining_cash[0]["cash"], total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # link user to buy page
    if request.method == "GET":
        return render_template("buy.html")

    # user submits buy form
    if request.method == "POST":
        # add based on user search
        symbol = request.form.get("symbol")

        # special case
        if symbol.upper() == "ORPH":
            return apology("SAY NO TO DRUGS", 69)

        # allow user to type in lower/ upper case
        stock = lookup(symbol.upper())

        # check if stock exists
        if not stock:
            flash("Ticker does not exist")
            return render_template("buy.html")

        # obtain number of shares
        quantity = request.form.get("shares")

        # check that user inputs number of shares
        if not quantity:
            flash("Must select quantity")
            return render_template("buy.html")

        # in case user bypasses form limitations and enter a string instead of a number
        if not quantity.isnumeric():
            flash("Number of shares should be an integer")
            return render_template("buy.html")

        # check that number of shares is positive
        quantity = int(quantity)
        if quantity < 1:
            flash("Minimum lot size: 1")
            return render_template("buy.html")

        # calculate cost of shares
        cost = stock["Price"] * quantity

        # update user's remaining cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        remaining_cash = user_cash[0]["cash"] - cost

        # check that user has sufficient cash
        if remaining_cash < 0:
            flash("Insufficient cash: check your cash value")
            return redirect("/")

        # if all checks pass, update user's holdings and cash
        else:
            db.execute("INSERT INTO holdings (user_id, symbol, name, price, shares, action) VALUES (?, ?, ?, ?, ?, ?)",
                       session["user_id"], stock["Symbol"], stock["Name"], stock["Price"], quantity, "Buy")
            db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, session["user_id"])

        flash("Transaction Completed")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    holdings = db.execute("SELECT * FROM holdings WHERE user_id = ? ORDER BY time DESC", session["user_id"])
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    return render_template("history.html", username=name[0]["username"], holdings=holdings)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/ or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # link to quote page
    if request.method == "GET":
        return render_template("quote.html")

    # when user submits search request
    elif request.method == "POST":
        symbol = request.form.get("symbol")

        # check that user has valid input
        if not symbol:
            flash("Input stock ticker")
            return render_template("quote.html")

        # check that ticker exists
        stocks = lookup(symbol.upper())
        if not stocks:
            flash("Ticker does not exist")
            return render_template("quote.html")

        # load quotation page
        else:
            return render_template("quoted.html", stock_name=stocks["Name"], stocks=stocks, stock_symbol=stocks["Symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """register user"""
    # link user to registration page
    if request.method == "GET":
        return render_template("register.html")

    # after user enters registration page and fills up details
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check if username has already been taken
        temp_database = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(temp_database) != 0:
            return apology("Error: Username already taken.", 400)

        # check if user has input a username
        if not username:
            return apology("Error: Please input a username", 400)

        # check if user has input a password
        if not password:
            return apology("Error: Please input a password", 400)

        # check if user has confirmed password
        if not confirmation:
            return apology("Error: Please confirm password", 400)

        # check if user confirmed password successfully
        if confirmation != password:
            return apology("Error: Password do not match", 400)

        hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        # update main database with user's login information
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # return to login page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT symbol FROM holdings WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    # link user to sell page
    if request.method == "GET":
        return render_template("sell.html", stocks=stocks)

    # user submits sell form
    if request.method == "POST":
        # remove based on user search
        symbol = request.form.get("symbol")

        # check that symbol exists
        if not symbol:
            flash("Select stock ticker")
            return render_template("sell.html", stocks=stocks)

        # allow user to type in lower/ upper case
        stock = lookup(symbol.upper())

        # check if stock exists
        if not stock:
            flash("Ticker does not exist")
            return render_template("sell.html", stocks=stocks)

        # generate user's holdings
        user_holdings = db.execute(
            "SELECT symbol, SUM(shares) as shares, total FROM holdings WHERE symbol = ? AND user_id = ? GROUP BY symbol", symbol, session["user_id"])

        # check that user currently holds the stock
        if len(user_holdings) == 0:
            flash("You do not own this stock: check your holdings")
            return redirect("/")

        quantity = request.form.get("shares")

        # check that user inputs number of shares
        if not quantity:
            flash("Must select quantity")
            return render_template("sell.html", stocks=stocks)

        # check that user does not sell more than amount owned.
        if int(quantity) > user_holdings[0]["shares"]:
            flash("You do not own sufficient shares: check your holdings")
            return redirect("/")

        # in case user bypasses form limitations and enter a string instead of a number
        if not quantity.isnumeric():
            flash("Number of shares should be an integer")
            return render_template("sell.html", stocks=stocks)

        # check that number of shares is positive
        quantity = int(quantity)
        if quantity < 1:
            flash("Minimum lot size: 1")
            return render_template("sell.html", stocks=stocks)

        # calculate earnings from sale
        earnings = stock["Price"] * quantity

        # update user's remaining cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        remaining_cash = user_cash[0]["cash"] + earnings

        # if all checks pass, update user's holdings and cash
        quantity = 0 - quantity
        db.execute("INSERT INTO holdings (user_id, symbol, name, price, shares, action) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], stock["Symbol"], stock["Name"], stock["Price"], quantity, "Sell")
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, session["user_id"])

        flash("Transaction Completed")
        return redirect("/")


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """top up account"""

    # obtain user information
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    holdings = db.execute("SELECT * FROM holdings WHERE user_id = ?", session["user_id"])

    # link to top-up site
    if request.method == "GET":
        return render_template("topup.html", user_username=users[0]["username"], user_cash=users[0]["cash"])

    # after submitting top-up request:
    if request.method == "POST":
        top_up_amount = request.form.get("top_up_amount")

        # ensure user has input
        if not top_up_amount:
            flash("Input top-up amount")
            return render_template("topup.html", user_username=users[0]["username"], user_cash=users[0]["cash"])

        # ensure user input is valid
        if not top_up_amount.isnumeric():
            flash("Invalid top-up amount, whole numbers only")
            return render_template("topup.html", user_username=users[0]["username"], user_cash=users[0]["cash"])

        # ensure user top-ups minimally 1000
        if int(top_up_amount) < 1000:
            flash("Minimum top-up: $1000")
            return render_template("topup.html", user_username=users[0]["username"], user_cash=users[0]["cash"])

        confirmation = request.form.get("confirmation")

        # ensure user has input
        if not confirmation:
            flash("Input confirmation")
            return render_template("topup.html", user_username=users[0]["username"], user_cash=users[0]["cash"])

        # ensure user confirms correctly
        if confirmation != top_up_amount:
            flash("Please confirm top-up amount again")
            return render_template("topup.html", user_username=users[0]["username"], user_cash=users[0]["cash"])

        else:
            # update user's cash
            new_cash = users[0]["cash"] + int(top_up_amount)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
            flash("Account value updated")
            return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """change password"""
    # obtain user information
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    # link to change password
    if request.method == "GET":
        return render_template("change_password.html", user_username=users[0]["username"])

    # after user submits change password request
    if request.method == "POST":
        # obtain passwords
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # check that user has input current password
        if not current_password:
            flash("Input current password")
            return render_template("change_password.html", user_username=users[0]["username"])

        # check that current password is user's password
        if not check_password_hash(users[0]["hash"], current_password):
            flash("Wrong password")
            return render_template("change_password.html", user_username=users[0]["username"])

        # check that user has input new password
        if not new_password:
            flash("Input new password")
            return render_template("change_password.html", user_username=users[0]["username"])

        # check that user has confirmed new password
        if not confirmation:
            flash("Confirm new password")
            return render_template("change_password.html", user_username=users[0]["username"])

        # check that confirmation is successful
        if confirmation != new_password:
            flash("Confirm new password again")
            return render_template("change_password.html", user_username=users[0]["username"])

        else:
            # generate hash and update user's password
            hash = generate_password_hash(new_password, method="pbkdf2:sha256", salt_length=8)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])
            flash("Password changed")
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
