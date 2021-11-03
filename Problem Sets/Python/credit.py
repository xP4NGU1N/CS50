import cs50
# prompt user for credit card number
number = cs50.get_int("Number: ")

# Luhn's Algorithm
temp = number
sum = 0
i = 1
while temp > 0:
    # seperate every other digit
    if i % 2 != 0:
        sum += (temp % 10)
    else:
        # check if digit x 2 will be larger than 10
        if temp % 10 > 4:
            sum += 1 + ((2 * (temp % 10)) % 10)
        else:
            sum += 2 * (temp % 10)
    temp = int(temp/10)
    i += 1

if sum % 10 != 0:
    print("INVALID")

# compare against card database
elif (number > 339999999999999 and number < 350000000000000) or (number > 369999999999999 and number < 380000000000000):
    print("AMEX")
    
elif number > 5099999999999999 and number < 5600000000000000:
    print("MASTERCARD")
    
elif (number > 3999999999999 and number < 5000000000000) or (number > 3999999999999999 and number < 5000000000000000):
    print("VISA")

else:
    print("INVALID")
    