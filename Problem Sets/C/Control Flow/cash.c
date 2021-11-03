#include <stdio.h>
#include <cs50.h>
#include <math.h>

int a, i;
float x;
float get_change();

int main(void)
{

    //obtain change in cents
    x = get_change();
    a = round(x * 100);
    
    //calculate minimum number of coins 
    for (i = 0; a > 0; i++)
    {
        if (a >= 25)
        {
            a -= 25;
        }
        else if (a < 25 && a >= 10)
        {
            a -= 10; 
        }
        else if (a < 10 && a >= 5)
        {
            a -= 5;
        }
        else
        {
            a -= 1;
        }
    }
    
    //output number of coins
    printf("%i\n", i);
}


// ensure change is positive value 
float get_change()
{
    float n;
    do 
    {
        n = get_float("Change owed: ");
    }
    while (n < 0);
    return n; 
}