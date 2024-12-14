def blink(stones):
    new_stones = []

    for stone in stones:
        # Rule 1: If the stone is 0, it becomes 1
        if stone == 0:
            new_stones.append(1)

        # Rule 2: If the stone has an even number of digits, it splits
        elif len(str(abs(stone))) % 2 == 0:
            stone_str = str(stone)
            mid = len(stone_str) // 2
            left_half = int(stone_str[:mid])
            right_half = int(stone_str[mid:])
            new_stones.append(left_half)
            new_stones.append(right_half)

        # Rule 3: Otherwise, multiply the stone by 2024
        else:
            new_stones.append(stone * 2024)

    return new_stones


def simulate_blinks(stones, blinks):
    for _ in range(blinks):
        stones = blink(stones)
    return stones


def read_input_from_file(filename):
    with open(filename, "r") as f:
        # Read the contents and convert to a list of integers
        stones = list(map(int, f.read().strip().split()))
    return stones


# Read input from the text file
filename = "input/day_eleven_input.txt"
initial_stones = read_input_from_file(filename)

# Specify the number of blinks
blinks = 25

# Simulate the blinks
result = simulate_blinks(initial_stones, blinks)

# Print the result
print("Stones after", blinks, "blinks:", len(result))
