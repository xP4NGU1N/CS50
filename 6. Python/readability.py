import cs50

letter_count = 0
word_count = 1
sentence_count = 0

text = cs50.get_string("Text: ")

for i in text:
    
    # covert character to ascii code
    code = ord(i)
    
    # check for alphabet
    if (code > 64 and code < 91) or (code > 96 and code < 123):
        letter_count += 1
    
    # check for space
    elif code == 32:
        word_count += 1
    # check for sentence ending punctuation
    elif (code == 33) or (code == 46) or (code == 63):
        sentence_count += 1

# Coleman-Liau index
L = (letter_count / word_count) * 100
S = (sentence_count / word_count) * 100
Index = round(0.0588 * L - 0.296 * S - 15.8)
if Index < 1: 
    print("Before Grade 1")

elif Index > 16:
    print("Grade 16+")

else:
    print(f"Grade {Index}")