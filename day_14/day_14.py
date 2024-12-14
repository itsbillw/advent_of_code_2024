import numpy as np

grid_width = 101
grid_height = 103


def print_grid(robots):
    """Print the grid with robot positions."""
    grid = np.zeros((grid_height, grid_width), dtype=int)

    # Place robots at their current positions
    for p_x, p_y, _, _ in robots:
        grid[p_y, p_x] += 1

    # Print the grid
    for row in grid:
        print(" ".join(str(cell) if cell > 0 else "." for cell in row))


def count_robots_in_quadrants(robots):
    """Count the robots in each quadrant after the grid is divided."""
    # Divide the grid into 4 quadrants
    # Find the middle rows and columns (ignore mid_x and mid_y)
    mid_x = grid_width // 2
    mid_y = grid_height // 2

    # Initialize the quadrant counts
    quadrant_counts = {
        "top_left": 0,
        "top_right": 0,
        "bottom_left": 0,
        "bottom_right": 0,
    }

    # Count robots in each quadrant
    for p_x, p_y, _, _ in robots:
        # Ignore robots on the central line (mid_x and mid_y)
        if p_x == mid_x or p_y == mid_y:
            continue

        if p_x < mid_x and p_y < mid_y:
            quadrant_counts["top_left"] += 1
        elif p_x >= mid_x and p_y < mid_y:
            quadrant_counts["top_right"] += 1
        elif p_x < mid_x and p_y >= mid_y:
            quadrant_counts["bottom_left"] += 1
        elif p_x >= mid_x and p_y >= mid_y:
            quadrant_counts["bottom_right"] += 1

    return quadrant_counts


def calculate_check_number(quadrant_counts):
    """Multiply the quadrant counts to get the check number."""
    return (
        quadrant_counts["top_left"]
        * quadrant_counts["top_right"]
        * quadrant_counts["bottom_left"]
        * quadrant_counts["bottom_right"]
    )


# Read the file and parse the robot positions and velocities
filename = "input/day_fourteen_input.txt"
robots = []

with open(filename, "r") as file:
    for line in file:
        parts = line.strip().split()
        p_str = parts[0].split("=")[1]
        v_str = parts[1].split("=")[1]

        p_x, p_y = map(int, p_str.split(","))
        v_x, v_y = map(int, v_str.split(","))
        robots.append((p_x, p_y, v_x, v_y))

# Simulate the movement of robots for a given number of seconds
seconds = 100

# Iterate for 'seconds' number of times
for t in range(seconds):
    # Move robots based on their velocities
    robots = [
        ((p_x + v_x) % grid_width, (p_y + v_y) % grid_height, v_x, v_y)
        for p_x, p_y, v_x, v_y in robots
    ]

# Print the grid after 'seconds + 1' iterations (i.e., after all robot movements)
print(f"After {seconds} second(s):")
print_grid(robots)

# Count robots in each quadrant
quadrant_counts = count_robots_in_quadrants(robots)
print("\nRobot count in each quadrant:")
for quadrant, count in quadrant_counts.items():
    print(f"{quadrant.capitalize()}: {count} robots")

# Calculate and print the check number
check_number = calculate_check_number(quadrant_counts)
print(f"\nCheck number: {check_number}")
