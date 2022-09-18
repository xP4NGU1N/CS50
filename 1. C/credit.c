#include <cs50.h>
#include <stdio.h>

int sum; 

int main(void)

{
    //obtain credit card number from user
    long n;
    n = get_long("Number: ");
    
    //save number to compare against card type
    long a = n;
    
    //Luhn's Algorithm
    sum = 0;
    for (int i = 0; n > 0; i++)
    {
        if (i % 2 != 0)
        {
            if (n % 10 > 4)
            {
                sum += ((2 * (n % 10)) % 10) + 1;
            }
            else
            {
                sum += (2 * (n % 10));
            }
            
            n = n / 10;
        }
        else 
        {
            sum += (n % 10);
            n = n / 10; 
        }
    }
    if (sum % 10 != 0)
    {
        printf("INVALID\n"); 
    }
    
    //check for brand of card
    else if (a > 339999999999999 && a < 350000000000000)
    {
        printf("AMEX\n");
    }
    else if (a > 369999999999999 && a < 380000000000000)
    {
        printf("AMEX\n");
    }
    else if (a > 5099999999999999 && a < 5600000000000000)
    {
        printf("MASTERCARD\n");
    }
    else if (a > 3999999999999 && a < 5000000000000)
    {
        printf("VISA\n");
    }
    else if (a > 3999999999999999 && a < 5000000000000000)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}