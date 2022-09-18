// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>
#include "dictionary.h"

int word_count = 0;
void empty();

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 800;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int correct = 0;
    // TODO: Compare word against dictionary
    int compare = hash(word);
    for (node *tmp = table[compare]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(word, tmp->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //TODO: Hash words based on sum of ASCII Code
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    //Ensure that sum does not exceed size of array
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO: Add words from dictionary into hash table
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file. \n");
        return false;
    }
    char test_word[45];
    while (fscanf(file, "%s", test_word) != EOF)
    {
        node *w = malloc(sizeof(node));
        if (w == NULL)
        {
            return false;
        }
        strcpy(w->word, test_word);
        
        //Point to the node that table was pointing to
        w->next = table[hash(test_word)];
        
        //Table now points to this new node
        table[hash(test_word)] = w;
        word_count ++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO: Return word_count
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO: Free all arrays of linked list
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }
    return true;
}