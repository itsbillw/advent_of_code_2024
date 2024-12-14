#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define INITIAL_CAPACITY 100

// Function to calculate number of digits in a number
int num_digits(int n) {
    if (n == 0) return 1;
    return (int)log10(n) + 1;
}

// Blink transformation
int* blink(int* stones, int* size, int* capacity) {
    int* new_stones = malloc(sizeof(int) * (*capacity));
    int new_size = 0;

    for (int i = 0; i < *size; i++) {
        int stone = stones[i];

        if (stone == 0) {
            new_stones[new_size++] = 1;
        } else {
            int stone_digits = num_digits(stone);
            if (stone_digits % 2 == 0) {
                // Split into two stones
                char buffer[20];
                sprintf(buffer, "%d", stone);
                int mid = strlen(buffer) / 2;

                int left = atoi(strndup(buffer, mid));
                int right = atoi(strndup(buffer + mid, strlen(buffer) - mid));
                new_stones[new_size++] = left;
                new_stones[new_size++] = right;
            } else {
                new_stones[new_size++] = stone * 2024;
            }
        }

        // Reallocate if new stones exceed capacity
        if (new_size >= *capacity) {
            *capacity *= 2;
            new_stones = realloc(new_stones, sizeof(int) * (*capacity));
        }
    }

    *size = new_size;
    free(stones);
    return new_stones;
}

// Function to simulate the blinks
int* simulate_blinks(int* stones, int* size, int blinks) {
    int capacity = INITIAL_CAPACITY;

    for (int i = 0; i < blinks; i++) {
        stones = blink(stones, size, &capacity);
    }

    return stones;
}

// Function to read the input from a file
int* read_input_from_file(char* filename, int* size) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error reading file");
        exit(1);
    }

    int* stones = malloc(sizeof(int) * INITIAL_CAPACITY);
    *size = 0;

    while (fscanf(file, "%d", &stones[*size]) != EOF) {
        (*size)++;
        if (*size % INITIAL_CAPACITY == 0) {
            stones = realloc(stones, sizeof(int) * (*size + INITIAL_CAPACITY));
        }
    }

    fclose(file);
    return stones;
}

int main() {
    char* filename = "input/day_eleven_sample.txt";
    int size;
    int* stones = read_input_from_file(filename, &size);

    int blinks = 75;
    stones = simulate_blinks(stones, &size, blinks);

    printf("Number of stones after %d blinks: %d\n", blinks, size);

    free(stones);
    return 0;
}
