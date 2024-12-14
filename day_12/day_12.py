import pandas as pd

# Read the garden plot map from the file
filename = "input/day_twelve_input.txt"
with open(filename) as f:
    garden_map = [list(line.strip()) for line in f]

# Convert the garden map to a pandas DataFrame
df = pd.DataFrame(garden_map)

# Directions for adjacent cells (up, down, left, right)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# Function to perform DFS and find a region
def dfs(x, y, plant_type, visited):
    stack = [(x, y)]
    area = 0
    perimeter = 0
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        area += 1
        # Check the 4 directions (up, down, left, right)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < df.shape[0] and 0 <= ny < df.shape[1]:  # within bounds
                if df.iloc[nx, ny] == plant_type:
                    if (nx, ny) not in visited:
                        stack.append((nx, ny))
                else:
                    perimeter += 1  # edge touching another region
            else:
                perimeter += 1  # edge touching the boundary
    return area, perimeter


# Main logic to find all regions and compute the total cost
visited: set[tuple[int, int]] = set()
total_cost = 0

for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        if (i, j) not in visited:
            plant_type = df.iloc[i, j]
            area, perimeter = dfs(i, j, plant_type, visited)
            cost = area * perimeter
            total_cost += cost

print(f"Total cost: {total_cost}")
