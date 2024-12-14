package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

// Optimized method to calculate the number of digits in a number without converting it to a string.
func numDigits(n int) int {
	if n == 0 {
		return 1
	}
	return int(math.Floor(math.Log10(float64(n))) + 1)
}

// Efficient blink transformation
func blink(stones []int) []int {
	// Create a new slice with sufficient capacity to minimize reallocations.
	var newStones []int
	newStones = newStones[:0] // Reset slice without reallocation.

	for _, stone := range stones {
		// Rule 1: If the stone is 0, it becomes 1
		if stone == 0 {
			newStones = append(newStones, 1)
		} else {
			// Rule 2: If the stone has an even number of digits, it splits
			if numDigits(stone)%2 == 0 {
				stoneStr := strconv.Itoa(stone)
				mid := len(stoneStr) / 2
				leftHalf, _ := strconv.Atoi(stoneStr[:mid])
				rightHalf, _ := strconv.Atoi(stoneStr[mid:])
				newStones = append(newStones, leftHalf, rightHalf)
			} else {
				// Rule 3: Otherwise, multiply the stone by 2024
				newStones = append(newStones, stone*2024)
			}
		}
	}
	return newStones
}

// Efficiently simulate the blinks
func simulateBlinks(stones []int, blinks int) []int {
	for i := 0; i < blinks; i++ {
		stones = blink(stones)
	}
	return stones
}

// Read the input from the file and return the slice of stones.
func readInputFromFile(filename string) ([]int, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	// Convert space-separated values to integers
	strData := strings.Fields(string(data))
	var stones []int
	for _, s := range strData {
		num, err := strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
		stones = append(stones, num)
	}

	return stones, nil
}

func main() {
	// Read input from the file
	filename := "input/day_eleven_sample.txt"
	initialStones, err := readInputFromFile(filename)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	// Specify the number of blinks
	blinks := 75

	// Simulate the blinks efficiently
	result := simulateBlinks(initialStones, blinks)

	// Print the length of the result (number of stones)
	fmt.Println("Number of stones after", blinks, "blinks:", len(result))
}
