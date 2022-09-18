#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int key;

int main(int argc, string argv[])
{
    //check if only 1 input
    if (argc != 2)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
    else if (argc == 2)
    {
        //check if imput is entirely digits
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key \n");
                return 1;
            }
        }
        //convert string to integer
        key = atoi(argv[1]);
    }
    
    //obtain plaintext
    string s = get_string("plaintext: ");
    
    //convert plaintext to ciphertext
    for (int j = 0, k = strlen(s); j < k; j++)
    {
        if (isupper(s[j]))
        {
            s[j] = ((s[j] - 65 + key) % 26 + 65);
        }
        else if (islower(s[j]))
        {
            s[j] = ((s[j] - 97 + key) % 26 + 97);
        }
        else
        {
            s[j] = s[j];
        }
    }
    printf("ciphertext: %s\n", s);
    return 0;
}


