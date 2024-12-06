package main

import (
	"bufio"
	"fmt"
	"os"
	"sync"
	"time"
)

type Position struct {
	Row, Col int
}

type State struct {
	Pos       Position
	Direction int // Use an integer for direction (0=up, 1=right, 2=down, 3=left)
}

// Movement deltas for directions
var moves = []Position{
	{-1, 0}, // up
	{0, 1},  // right
	{1, 0},  // down
	{0, -1}, // left
}

func readGridFromFile(filename string) ([][]rune, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var grid [][]rune
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		grid = append(grid, []rune(line))
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return grid, nil
}

// Simulate guard movement and detect loops
func simulate(grid [][]rune, start Position, direction int, obstruction Position) bool {
	rows, cols := len(grid), len(grid[0])
	visited := make(map[State]bool)
	current := start
	currentDirection := direction
	maxSteps := 2 * rows * cols
	stepCount := 0

	// Create a copy of the grid for this simulation
	gridCopy := make([][]rune, rows)
	for i := range grid {
		gridCopy[i] = append([]rune{}, grid[i]...)
	}

	// Place the obstruction
	gridCopy[obstruction.Row][obstruction.Col] = 'O'

	for stepCount < maxSteps {
		state := State{current, currentDirection}
		if visited[state] {
			return true // Loop detected
		}
		visited[state] = true

		// Calculate next position
		next := Position{
			Row: current.Row + moves[currentDirection].Row,
			Col: current.Col + moves[currentDirection].Col,
		}

		// Check boundaries
		if next.Row < 0 || next.Row >= rows || next.Col < 0 || next.Col >= cols {
			return false // Exited the grid
		}

		// Check for obstacles
		if gridCopy[next.Row][next.Col] == '#' || gridCopy[next.Row][next.Col] == 'O' {
			currentDirection = (currentDirection + 1) % 4 // Turn 90 degrees clockwise
			continue
		}

		// Move to the next position
		current = next
		stepCount++
	}

	return false // No loop detected
}

// Find all valid positions for obstruction
func findObstructionPositions(grid [][]rune, start Position, direction int) []Position {
	rows, cols := len(grid), len(grid[0])
	var wg sync.WaitGroup
	var mu sync.Mutex
	validPositions := []Position{}

	// Limit the number of goroutines to avoid excessive memory usage
	sem := make(chan struct{}, 16) // Semaphore for limiting concurrency

	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if (r != start.Row || c != start.Col) && grid[r][c] == '.' {
				wg.Add(1)
				sem <- struct{}{} // Acquire semaphore
				go func(row, col int) {
					defer wg.Done()
					defer func() { <-sem }() // Release semaphore
					obstruction := Position{row, col}
					if simulate(grid, start, direction, obstruction) {
						mu.Lock()
						validPositions = append(validPositions, obstruction)
						mu.Unlock()
					}
				}(r, c)
			}
		}
	}

	wg.Wait()
	return validPositions
}

func main() {
	// Timer start
	startTime := time.Now()

	// File containing the input grid
	filename := "input/day_six_input.txt"

	// Read grid from file
	grid, err := readGridFromFile(filename)
	if err != nil {
		fmt.Println("Error reading grid:", err)
		return
	}

	// Find guard's starting position and direction
	var start Position
	var direction int
	found := false
	for r := 0; r < len(grid) && !found; r++ {
		for c := 0; c < len(grid[r]) && !found; c++ {
			switch grid[r][c] {
			case '^':
				start = Position{r, c}
				direction = 0 // up
				found = true
			case '>':
				start = Position{r, c}
				direction = 1 // right
				found = true
			case 'v':
				start = Position{r, c}
				direction = 2 // down
				found = true
			case '<':
				start = Position{r, c}
				direction = 3 // left
				found = true
			}
		}
	}

	// Find all valid obstruction positions
	validPositions := findObstructionPositions(grid, start, direction)

	// Timer end
	elapsed := time.Since(startTime)

	// Output the results
	fmt.Printf("Number of valid positions for obstruction: %d in %.2f seconds\n", len(validPositions), elapsed.Seconds())
}
