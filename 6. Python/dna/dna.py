import cs50
import sys
import csv

# ensure correct usage
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")

# compile DNA into a list
DNA = []
with open(sys.argv[1], "r") as file:
    reader = csv.reader(file)
    for row in reader:
        DNA.append(row)

# read DNA sequence into a string
with open(sys.argv[2], "r") as file_2:
    reader_2 = file_2.read()

# record highest number of consecutive STR
Max_count = []

# one STR at a time
for i in range(1, len(DNA[0])):
    Max_count.append(0)
    STR = DNA[0][i]
    
    # slice DNA sequence into length of STR for comparison    
    for j in range(len(reader_2) - len(STR) + 1):
        STR_count = 0
        test = reader_2[(j):(j + len(STR))]
        
        # once match with a STR:  
        if test == STR:
            k = 0
            
            # check for consecutive STR
            while (reader_2[(j + k):(j + k + len(STR))]) == STR:
                k += len(STR)
                STR_count += 1
                
            # check for longest consecutive STR
            if STR_count > Max_count[i - 1]:
                Max_count[i - 1] = STR_count

# compare against database (DNA)
for x in range(1, len(DNA)):
    Match = 0
    for y in range(1, len(DNA[0])):
        if Max_count[y - 1] == int(DNA[x][y]):
            Match += 1
            
    # check if all STR counts from DNA sequence matches that in DNA list
    if Match == (len(DNA[0]) - 1):
        print(f"{DNA[x][0]}")
        exit(0)

print("No Match")