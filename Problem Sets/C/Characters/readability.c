#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");

    float letter_count = 0;
    float word_count = 1;
    float sentence_count = 0;

    // read through string
    for (int i = 0; i < strlen(text); i++)
    {
        // if character is an alphabet
        if ((text[i] > 64 && text[i] < 91) || (text[i] > 96 && text[i] < 123))
        {
            letter_count++;
        }
        
        // if character is a space
        else if (text[i] == 32)
        {
            word_count++;
        }
        
        // if character is a sentence ending punctuation  
        else if ((text[i] == 33) || (text[i] == 46) || (text[i] == 63))
        {
            sentence_count++;
        }
    }
    printf("%f\n", letter_count);
    // Coleman-Liau index
    float L = (letter_count / word_count) * 100;
    float S = (sentence_count / word_count) * 100;
    int Index = round((0.0588 * L) - (0.296 * S) - 15.8);
    if (Index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (Index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", Index);
    }
}