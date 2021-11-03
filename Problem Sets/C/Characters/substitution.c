#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int n, a, x, j, k;

int main(int argc, string argv[])
{
    //check if only 1 input
    if (argc != 2)
    {
        printf("Usage: ./substitution key \n");
        return 1;
    }
    //check if only 26 characters
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        for (a = 0, n = strlen(argv[1]); a < n; a++)
            //check if all characters are alphabets
        {
            if (!isalpha(argv[1][a]))
            {
                printf("Key must contain 26 characters.\n");
                return 1;
            }
            else
                //check if all alphabets are unique
            {
                for (x = a + 1; x < n; x++)
                {
                    if (argv[1][a] == argv[1][x])
                    {
                        printf("Key must contain 26 unique characters.\n");
                        return 1;
                    }
                }
            }
        }
    }

    //obtain plaintext
    string s = get_string("plaintext: ");

    //convert plaintext to ciphertext
    for (j = 0, k = strlen(s); j < k; j++)
    {
        if (isupper(s[j]))
        {
            s[j] = toupper(argv[1][s[j] - 65]);
        }
        if (islower(s[j]))
        {
            s[j] = tolower(argv[1][s[j] - 97]);
        }
        else
        {
            s[j] = s[j];
        }
    }

    printf("ciphertext: %s\n", s);
    return 0;
}