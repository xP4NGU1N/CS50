#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int a = 0; a < height; a++)
    {
        for (int i = 0; i < width; i++)
        {
            float average = round((image[a][i].rgbtRed + image[a][i].rgbtGreen + image[a][i].rgbtBlue) / 3.0);
            image[a][i].rgbtGreen = image[a][i].rgbtBlue = image[a][i].rgbtRed = average;
        }
    }
    return;
}


// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int counter;
    float red, green, blue;
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            counter = 0;
            red = 0;
            green = 0;
            blue = 0;
            for (int a = i - 1; a < i + 2; a++)
            {
                for (int b = j - 1; b < j + 2; b++)
                {
                    // Check if pixel exists
                    if ((a >= 0) && (a <= height - 1) && (b >= 0) && (b <= width - 1))
                    {
                        counter++;
                        red += image[a][b].rgbtRed;
                        green += image[a][b].rgbtGreen;
                        blue += image[a][b].rgbtBlue;
                    }
                }
            }
            // Store blurred pixel in temporary array
            temp[i][j].rgbtRed = round(red / counter);
            temp[i][j].rgbtGreen = round(green / counter);
            temp[i][j].rgbtBlue = round(blue / counter);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}


// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    float xred, xgreen, xblue, yred, ygreen, yblue;
    RGBTRIPLE temp[height][width];
    int sobelred, sobelgreen, sobelblue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            xred = 0;
            xgreen = 0;
            xblue = 0;
            yred = 0;
            ygreen = 0;
            yblue = 0;
            for (int a  = i - 1; a < i + 2; a++)
            {
                for (int b = j - 1; b < j + 2; b++)
                {
                    // Check if pixel exists
                    if ((a >= 0) && (a <= height - 1) && (b >= 0) && (b <= width - 1))
                    {
                        // Gather values based on Gx pattern
                        if (a == i)
                        {
                            xred += 2 * (b - j) * image[a][b].rgbtRed;
                            xgreen += 2 * (b - j) * image[a][b].rgbtGreen;
                            xblue += 2 * (b - j) * image[a][b].rgbtBlue;
                        }
                        if (a != i)
                        {
                            xred += (b - j) * image[a][b].rgbtRed;
                            xgreen += (b - j) * image[a][b].rgbtGreen;
                            xblue += (b - j) * image[a][b].rgbtBlue;
                        }
                        // Gather values based on Gy pattern
                        if (b == j)
                        {
                            yred += 2 * (a - i) * image[a][b].rgbtRed;
                            ygreen += 2 * (a - i) * image[a][b].rgbtGreen;
                            yblue += 2 * (a - i) * image[a][b].rgbtBlue;

                        }
                        if (b != j)
                        {
                            yred += (a - i) * image[a][b].rgbtRed;
                            ygreen += (a - i) * image[a][b].rgbtGreen;
                            yblue += (a - i) * image[a][b].rgbtBlue;
                        }
                    }
                }
            }
            // Sobel filter algorithm
            sobelred = round(sqrt(xred * xred + yred * yred));
            if (sobelred > 255)
            {
                sobelred = 255;
            }
            sobelgreen = round(sqrt(xgreen * xgreen + ygreen * ygreen));
            if (sobelgreen > 255)
            {
                sobelgreen = 255;
            }
            sobelblue = round(sqrt(xblue * xblue + yblue * yblue));
            if (sobelblue > 255)
            {
                sobelblue = 255;
            }
            // Store pixel in temporary array
            temp[i][j].rgbtRed = sobelred;
            temp[i][j].rgbtGreen = sobelgreen;
            temp[i][j].rgbtBlue = sobelblue;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}
