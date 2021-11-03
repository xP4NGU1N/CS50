#include <cs50.h>
#include <stdio.h>

int get_starting_int(void);
int get_ending_int(void);

int x, y;

int main(void)

{
//obtain initial and ending population size
    x = get_starting_int();

    y = get_ending_int();
    
//counting the number of years    
    int i = 0;
    while (x < y)
    {
        x = x - x / 4 + x / 3 ;
        i++;
    }
    printf("Years: %i\n", i);
}




//ensure starting population is 9 and above
int get_starting_int(void)
{
    int n;
    do
    {
        n = get_int("Starting Population:  ");
    }
    while (n < 9);
    return n;
}    

//ensure ending population is larger than starting population
int get_ending_int(void)
{
    int n;
    do
    {
        n = get_int("Ending Population:  ");
    }
    while (n < x); 
    return n;
}