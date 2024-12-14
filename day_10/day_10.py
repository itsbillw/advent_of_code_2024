from collections import deque


# Helper function to check if a position is valid
def is_valid(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


# BFS function to count the number of reachable '9's from a trailhead
def bfs(grid, start_x, start_y, rows, cols):
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start_x, start_y)])
    visited = set([(start_x, start_y)])
    reachable_9s = 0

    while queue:
        x, y = queue.popleft()

        # If we reach a '9', increment the count
        if grid[x][y] == "9":
            reachable_9s += 1

        # Explore neighbors (up, down, left, right)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, rows, cols) and (nx, ny) not in visited:
                if int(grid[nx][ny]) == int(grid[x][y]) + 1:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    return reachable_9s


# Main function to calculate the sum of all trailhead scores
def trailhead_scores(grid):
    rows = len(grid)
    cols = len(grid[0])
    total_score = 0

    # Loop through all positions in the grid to find trailheads (positions with height 0)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "0":  # trailhead found
                # Perform BFS to count reachable '9's
                score = bfs(grid, i, j, rows, cols)
                total_score += score

    return total_score


# Function to read the grid from the input file
def read_grid_from_file(filename):
    with open(filename, "r") as file:
        grid = [list(line.strip()) for line in file]
    return grid


# Load the grid from the specified file
filename = "input/day_ten_input.txt"
grid = read_grid_from_file(filename)

# Calculate and print the total score
result = trailhead_scores(grid)
print(f"Total score: {result}")
