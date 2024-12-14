import pandas as pd
from collections import deque

# Read the garden plot map from the file
filename = "input/day_twelve_sample.txt"
with open(filename) as f:
    garden_map = [list(line.strip()) for line in f]

# Convert the garden map to a pandas DataFrame
df = pd.DataFrame(garden_map)

# Directions for adjacent cells (up, down, left, right)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# Function to perform BFS and find a region
def bfs(
    x: int,
    y: int,
    plant_type: str,
    visited: set[tuple[int, int]],
) -> tuple[int, int]:
    queue = deque([(x, y)])
    area = 0
    sides = 0  # Number of external sides for this region
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        area += 1
        # Check the 4 directions (up, down, left, right)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < df.shape[0] and 0 <= ny < df.shape[1]:  # within bounds
                if df.iloc[nx, ny] == plant_type and (nx, ny) not in visited:
                    queue.append((nx, ny))
                elif df.iloc[nx, ny] != plant_type:
                    sides += 1  # boundary with a different region
            else:
                sides += 1  # boundary with the grid edge
    return area, sides


# Main logic to find all regions and compute the total cost
visited: set[tuple[int, int]] = set()  # Annotate visited as a set of tuples (int, int)
total_cost = 0

# Loop through the entire garden map
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        if (i, j) not in visited:
            plant_type = df.iloc[i, j]
            area, sides = bfs(i, j, plant_type, visited)
            cost = area * sides  # Calculate cost for each isolated region

            # Trace the calculation for this region
            print(f"Region {plant_type}:")
            print(f"  Area: {area}")
            print(f"  Sides: {sides}")
            print(f"  Cost: {cost}")
            print("-" * 20)

            total_cost += cost

print(f"Total cost: {total_cost}")
