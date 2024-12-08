import pandas as pd

# Read the input map from a file
filename = "input/day_eight_input.txt"
with open(filename) as f:
    input_map = [line.strip() for line in f]

# Convert the input map to a pandas DataFrame
grid = pd.DataFrame([list(row) for row in input_map])


def find_antennas(grid):
    """Find all antennas grouped by frequency."""
    antennas_by_freq = {}
    for row_idx, row in grid.iterrows():
        for col_idx, cell in row.items():
            if cell.isalnum():  # Antennas are alphanumeric
                if cell not in antennas_by_freq:
                    antennas_by_freq[cell] = []
                antennas_by_freq[cell].append((row_idx, col_idx))
    return antennas_by_freq


def calculate_antinodes_with_harmonics(antennas_by_freq, rows, cols):
    """Calculate all antinode positions considering resonant harmonics."""
    antinodes = set()
    for freq, positions in antennas_by_freq.items():
        # If only one antenna of this frequency, no additional antinodes
        if len(positions) < 2:
            continue

        # Add all antenna positions of this frequency as antinodes
        antinodes.update(positions)

        # Check for aligned antinodes
        for i, (x1, y1) in enumerate(positions):
            for j, (x2, y2) in enumerate(positions):
                if i >= j:  # Avoid redundant comparisons
                    continue

                # Check if aligned
                dx, dy = x2 - x1, y2 - y1
                gcd = (
                    abs(dx)
                    if dy == 0
                    else abs(dy)
                    if dx == 0
                    else abs(gcd_recursive(dx, dy))
                )
                dx, dy = dx // gcd, dy // gcd  # Normalize direction vector

                # Extend in both directions to find antinodes
                nx, ny = x1, y1
                while 0 <= nx < rows and 0 <= ny < cols:
                    antinodes.add((nx, ny))
                    nx -= dx
                    ny -= dy
                nx, ny = x2, y2
                while 0 <= nx < rows and 0 <= ny < cols:
                    antinodes.add((nx, ny))
                    nx += dx
                    ny += dy

    return antinodes


def gcd_recursive(a, b):
    """Calculate GCD using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


# Find all antennas grouped by frequency
antennas_by_freq = find_antennas(grid)

# Map dimensions
rows, cols = grid.shape

# Calculate antinodes with updated conditions
antinodes = calculate_antinodes_with_harmonics(antennas_by_freq, rows, cols)

# Count unique antinode positions
unique_antinode_count = len(antinodes)

print(f"Number of unique antinode positions: {unique_antinode_count}")
