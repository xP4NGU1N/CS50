import cs50
# prompt user for change
while True:
    change = cs50.get_float("Change owed: ")
    if change > 0: 
        break

# convert to cents to avoid using floating values
cents = change * 100

# subtract 25 until <25
quarters = int(cents/25)
cents -= quarters * 25

# subtract 10 until <10
dimes = int(cents/10)
cents -= dimes * 10

# subtract 5 until <5
nickels = int(cents/5)
cents -= nickels * 5

pennies = int(cents)

print(f"{quarters + dimes + nickels + pennies}")
