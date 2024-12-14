import math
import re


# Function to read input and parse the data
def read_input(filename):
    with open(filename) as f:
        data = f.read().strip().split("\n\n")
    machines = []
    for entry in data:
        lines = entry.splitlines()

        # Parse the movements for Button A
        match_a = re.search(r"Button A: X([+-]?\d+), Y([+-]?\d+)", lines[0])
        X_a, Y_a = int(match_a.group(1)), int(match_a.group(2))

        # Parse the movements for Button B
        match_b = re.search(r"Button B: X([+-]?\d+), Y([+-]?\d+)", lines[1])
        X_b, Y_b = int(match_b.group(1)), int(match_b.group(2))

        # Parse the prize location
        match_prize = re.search(r"Prize: X=(\d+), Y=(\d+)", lines[2])
        prize_x, prize_y = int(match_prize.group(1)), int(match_prize.group(2))

        machines.append(((X_a, Y_a), (X_b, Y_b), (prize_x, prize_y)))

    return machines


# Function to calculate the minimum token cost for a machine
def calculate_min_cost(button_a, button_b, prize):
    X_a, Y_a = button_a
    X_b, Y_b = button_b
    prize_x, prize_y = prize

    # Try every combination of button presses a and b from 0 to 100
    min_cost = math.inf
    for a in range(101):  # a can be from 0 to 100
        for b in range(101):  # b can be from 0 to 100
            # Check if the combination aligns the claw to the prize
            if a * X_a + b * X_b == prize_x and a * Y_a + b * Y_b == prize_y:
                cost = a * 3 + b * 1  # 3 tokens for A press, 1 token for B press
                min_cost = min(min_cost, cost)

    return min_cost if min_cost != math.inf else None


# Function to solve the problem
def solve(filename):
    machines = read_input(filename)
    total_prizes = 0
    total_tokens = 0

    # Try to win as many prizes as possible
    for button_a, button_b, prize in machines:
        min_cost = calculate_min_cost(button_a, button_b, prize)
        if min_cost is not None:
            total_prizes += 1
            total_tokens += min_cost

    return total_prizes, total_tokens


# Main execution
filename = "input/day_thirteen_input.txt"
total_prizes, total_tokens = solve(filename)

print(f"Total prizes: {total_prizes}")
print(f"Total tokens: {total_tokens}")
