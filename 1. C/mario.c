#include <cs50.h>
#include <stdio.h>

int x;
int get_height_int(void);

int main(void)
{
    //Request for height from user
    x = get_height_int();

    //Build Pyramid
    for (int i = 0; i < x; i++)
    {
        //Align right
        for (int a = x; a > i + 1; a--)
        {
            printf(" ");
        }

        //Print each layer
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        printf("  ");

        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}


//Ensure height is between 1-8
int get_height_int(void)
{
    int n;
    do
    {
        n = get_int("Height:  ");
    }
    while (n < 1 || n > 8);
    return n;
}