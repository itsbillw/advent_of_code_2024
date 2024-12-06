import pandas as pd

# Example input grid (replace with your actual input)
filename = "input/day_six_input.txt"
with open(filename) as f:
    grid = [list(line.strip()) for line in f]

# Convert grid to DataFrame
df = pd.DataFrame(grid)

# Characters and their directions
directions = {"^": "up", "v": "down", "<": "left", ">": "right"}
direction_order = ["up", "right", "down", "left"]  # Clockwise order

# Find locations of target characters
locations = []
for char, direction in directions.items():
    char_locations = df.stack()[df.stack() == char].index.tolist()
    for loc in char_locations:
        locations.append((*loc, direction))

# Movement deltas for each direction
moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


# Function to simulate movement
def simulate_movement(grid, start, direction):
    visited = set()  # Track unique locations visited
    current = start
    current_direction = direction

    while True:
        visited.add(current)

        # Calculate the next move
        next_move = (
            current[0] + moves[current_direction][0],
            current[1] + moves[current_direction][1],
        )

        # Check for boundaries
        if (
            next_move[0] < 0
            or next_move[0] >= grid.shape[0]
            or next_move[1] < 0
            or next_move[1] >= grid.shape[1]
        ):
            break  # Stop if the next move is out of bounds

        # Check for obstacles
        if grid.loc[next_move[0], next_move[1]] == "#":
            # Turn 90 degrees clockwise
            current_direction = direction_order[
                (direction_order.index(current_direction) + 1) % 4
            ]
            continue

        # Update current position
        current = next_move

    return visited


# Simulate for each initial location and direction
results = []
all_visited = set()  # Collect all visited locations for visualization

for loc in locations:
    row, col, direction = loc
    visited = simulate_movement(df, (row, col), direction)
    all_visited.update(visited)
    results.append(len(visited))

# Print the total unique locations visited
print(f"Total Unique Locations Visited: {len(all_visited)}")

"""
# Mark visited locations on a copy of the grid
visualized_grid = df.copy()
for row, col in all_visited:
    visualized_grid.loc[row, col] = "X"

# Print the visualized grid
print("\nGrid with Visited Locations Marked:")
for row in visualized_grid.values:
    print("".join(row))
"""
