import pandas as pd

# Read the input map from a file
filename = "input/day_eight_input.txt"
with open(filename) as f:
    input_map = [line.strip() for line in f]

# Convert the input map to a pandas DataFrame
grid = pd.DataFrame([list(row) for row in input_map])


def find_antennas(grid):
    """Find all antennas and their positions."""
    antennas = []
    for row_idx, row in grid.iterrows():
        for col_idx, cell in row.items():
            if cell.isalnum():  # Antennas are alphanumeric
                antennas.append((cell, row_idx, col_idx))
    return antennas


def calculate_antinodes(antennas, rows, cols):
    """Calculate all antinode positions."""
    antinodes = set()
    for i in range(len(antennas)):
        freq1, x1, y1 = antennas[i]
        for j in range(len(antennas)):
            if i == j:
                continue  # Skip comparing the same antenna
            freq2, x2, y2 = antennas[j]
            if freq1 == freq2:
                # Antinodes occur at positions where one is twice as far
                dx, dy = x2 - x1, y2 - y1
                # Check for antinode positions
                antinode1 = (x1 - dx, y1 - dy)  # On the other side of the first antenna
                antinode2 = (
                    x2 + dx,
                    y2 + dy,
                )  # On the other side of the second antenna

                # Add only if within bounds
                if 0 <= antinode1[0] < rows and 0 <= antinode1[1] < cols:
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < rows and 0 <= antinode2[1] < cols:
                    antinodes.add(antinode2)
    return antinodes


# Get all antennas
antennas = find_antennas(grid)

# Map dimensions
rows, cols = grid.shape

# Calculate antinodes
antinodes = calculate_antinodes(antennas, rows, cols)

# Count unique antinode positions
unique_antinode_count = len(antinodes)

print(f"Number of unique antinode positions: {unique_antinode_count}")
