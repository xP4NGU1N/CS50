import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/submit", methods = ["GET", "POST"])
def submit():
    # TODO: Add the user's entry into the database
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")
    db.execute("INSERT INTO birthdays (name, month, day) VALUES (?,?,?)", name, month, day)
    return redirect("/birthdays")


@app.route("/birthdays")
def birthdays():
    birthdays = db.execute("SELECT * FROM birthdays")
    return render_template("birthdays.html", birthdays = birthdays)



