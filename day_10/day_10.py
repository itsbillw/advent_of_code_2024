# Helper function to check if a position is valid
def is_valid(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


# DFS function to find unique paths from a trailhead to a '9'
def dfs(grid, x, y, rows, cols, path, all_paths):
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # If we reach a '9', add the current path as a valid unique path
    if grid[x][y] == "9":
        all_paths.append(path[:])  # Store a copy of the current path
        return

    # Explore neighbors (up, down, left, right)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, rows, cols) and (nx, ny) not in path:
            if int(grid[nx][ny]) == int(grid[x][y]) + 1:
                path.append((nx, ny))
                dfs(grid, nx, ny, rows, cols, path, all_paths)
                path.pop()  # Backtrack


# Main function to calculate the sum of all trailhead ratings
def trailhead_ratings(grid):
    rows = len(grid)
    cols = len(grid[0])
    total_rating = 0

    # Loop through all positions in the grid to find trailheads (positions with height 0)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "0":  # Trailhead found
                all_paths = []
                # Perform DFS to find all unique paths from trailhead to '9'
                dfs(grid, i, j, rows, cols, [(i, j)], all_paths)
                # Count the number of unique paths for this trailhead
                trailhead_rating = len(all_paths)
                total_rating += trailhead_rating

    return total_rating


# Function to read the grid from the input file
def read_grid_from_file(filename):
    with open(filename, "r") as file:
        grid = [list(line.strip()) for line in file]
    return grid


# Load the grid from the specified file
filename = "input/day_ten_input.txt"
grid = read_grid_from_file(filename)

# Calculate and print the total rating
result = trailhead_ratings(grid)
print(f"Total rating: {result}")
