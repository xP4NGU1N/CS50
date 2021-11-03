#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //check for one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    //check and open forensic file
    FILE *image = fopen(argv[1], "r");
    if (image == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    
    //work with opened file
    BYTE buffer[512];
    int count = 0;
    char filename[8];
    FILE *jpeg = NULL;
    
    //check for EOF
    //read one block of data at a time (512 bytes)
    while (fread(&buffer, 512, 1, image) == 1)
    {   
        //jpeg file type detected
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {   
            //if new image found, close previous image first
            if (count > 0)
            {
                fclose(jpeg);
            }
            //name recovered files
            sprintf(filename, "%03i.jpg", count);
            jpeg = fopen(filename, "w");
            count++;
        }
        //keep transferring blocks of data until a new image is found
        if (count > 0)
        {
            fwrite(&buffer, 512, 1, jpeg);
        }
    }
    fclose(jpeg);
    fclose(image);
}