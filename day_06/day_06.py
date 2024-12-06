import pandas as pd

# Example input grid
filename = "input/day_six_input.txt"
with open(filename) as f:
    grid = [list(line.strip()) for line in f]

# Convert grid to DataFrame
df = pd.DataFrame(grid)

# Movement deltas for directions
directions = {"^": "up", "v": "down", "<": "left", ">": "right"}
direction_order = ["up", "right", "down", "left"]  # Clockwise order
moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

# Find guard's starting position and direction
guard_position = None
guard_direction = None
for char, direction in directions.items():
    positions = df.stack()[df.stack() == char].index.tolist()
    if positions:
        guard_position = positions[0]
        guard_direction = direction
        break


# Simulate guard movement with loop detection
def simulate_with_obstruction(grid, start, direction):
    visited = set()  # Track visited states (position, direction)
    current = start
    current_direction = direction
    max_steps = grid.size * 2  # Limit steps to prevent infinite loops
    step_count = 0

    while step_count < max_steps:
        state = (current, current_direction)
        if state in visited:
            return True  # Loop detected
        visited.add(state)

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
            return False  # Exited the grid

        # Check for obstacles
        if grid.loc[next_move[0], next_move[1]] in ["#", "O"]:
            # Turn 90 degrees clockwise
            current_direction = direction_order[
                (direction_order.index(current_direction) + 1) % 4
            ]
            continue

        # Update position and increment step count
        current = next_move
        step_count += 1

    return False  # No loop detected within the step limit


# Test all possible placements of `O`
valid_obstruction_positions = []
for r in range(df.shape[0]):
    for c in range(df.shape[1]):
        if (r, c) != guard_position and df.loc[r, c] == ".":
            # Place the obstruction and test
            df.loc[r, c] = "O"
            if simulate_with_obstruction(df, guard_position, guard_direction):
                valid_obstruction_positions.append((r, c))
            # Remove the obstruction
            df.loc[r, c] = "."

# Output results
print("Number of valid positions for obstruction:", len(valid_obstruction_positions))
print("Valid positions:", valid_obstruction_positions)
