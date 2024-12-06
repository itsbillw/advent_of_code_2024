import time
from collections import deque

import numpy as np
from joblib import Parallel, delayed
from numba import njit

# Example input grid
filename = "input/day_six_input.txt"
with open(filename) as f:
    grid = [list(line.strip()) for line in f]

# Convert grid to NumPy array
grid = np.array(grid)

# Movement deltas (precomputed arrays for Numba compatibility)
direction_order = np.array(["up", "right", "down", "left"])
moves = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])  # up, right, down, left
direction_indices = {"up": 0, "right": 1, "down": 2, "left": 3}


# Numba-accelerated simulation function
@njit
def simulate_with_obstruction_numba(grid, start, direction_index, obstruction, moves):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols, 4), dtype=np.bool_)  # Track visited states
    current_r, current_c = start
    current_direction = direction_index
    max_steps = rows * cols * 2  # Limit steps to prevent infinite loops
    step_count = 0

    # Place the obstruction
    grid[obstruction[0], obstruction[1]] = ord("O")

    while step_count < max_steps:
        if visited[current_r, current_c, current_direction]:
            grid[obstruction[0], obstruction[1]] = ord(".")  # Reset the grid
            return True  # Loop detected
        visited[current_r, current_c, current_direction] = True

        # Calculate the next move
        dr, dc = moves[current_direction]
        next_r, next_c = current_r + dr, current_c + dc

        # Check for boundaries
        if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
            grid[obstruction[0], obstruction[1]] = ord(".")  # Reset the grid
            return False  # Exited the grid, no loop

        # Check for obstacles
        if grid[next_r, next_c] in [ord("#"), ord("O")]:
            # Turn 90 degrees clockwise
            current_direction = (current_direction + 1) % 4
            continue

        # Update position and increment step count
        current_r, current_c = next_r, next_c
        step_count += 1

    grid[obstruction[0], obstruction[1]] = ord(".")  # Reset the grid
    return False  # No loop detected


# BFS for reachable cells
def reachable_cells(grid, start):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=np.bool_)
    queue = deque([start])
    reachable = []

    while queue:
        r, c = queue.popleft()
        if visited[r, c] or chr(grid[r, c]) in ["#", "O"]:
            continue
        visited[r, c] = True
        reachable.append((r, c))

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                queue.append((nr, nc))

    return reachable


# Multi-processing with joblib
def find_valid_positions(grid, start, direction_index, reachable):
    batch_size = max(1, len(reachable) // 10)  # Dynamically adjust batch size
    results = Parallel(n_jobs=-1, batch_size=batch_size)(
        delayed(simulate_with_obstruction_numba)(
            grid,
            start,
            direction_index,
            obstruction,
            moves,
        )
        for obstruction in reachable
        if obstruction != start and chr(grid[obstruction[0], obstruction[1]]) == "."
    )

    # Filter results where loops were detected
    valid_positions = [reachable[i] for i, result in enumerate(results) if result]
    return valid_positions


# Preprocess the grid for Numba compatibility
grid = np.vectorize(ord)(grid)  # Convert characters to integers for Numba

# Start the timer
start_time = time.time()

# Find guard's starting position and direction
guard_position = None
guard_direction = None
for char, direction in {"^": "up", "v": "down", "<": "left", ">": "right"}.items():
    positions = np.argwhere(grid == ord(char))
    if positions.size > 0:
        guard_position = tuple(positions[0])
        guard_direction = direction_indices[direction]  # Pass index instead of string
        break

# Find reachable cells and valid positions
reachable = reachable_cells(grid, guard_position)
valid_obstruction_positions = find_valid_positions(
    grid,
    guard_position,
    guard_direction,
    reachable,
)

# End the timer
end_time = time.time()

# Output results
print(
    f"Number of valid positions for obstruction: {len(valid_obstruction_positions)} "
    f"in {end_time - start_time:.2f} seconds",
)
