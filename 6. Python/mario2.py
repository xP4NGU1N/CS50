import cs50
# prompt user for height
while True:
    height = cs50.get_int("height: ")
    if height > 0 and height < 9:
        break

for j in range(1, height + 1):
    print((height - j) * " " + j * "#" + "  " + j * "#")
