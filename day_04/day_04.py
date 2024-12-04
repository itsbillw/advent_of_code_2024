def find_xmas_count(input_file, pattern):
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Convert the lines into a 2D array of characters
    grid = [list(line.strip()) for line in lines]

    # Define the possible directions to check
    directions = [
        (0, 1),  # right
        (1, 0),  # down
        (1, 1),  # diagonal down-right
        (-1, 1),  # diagonal up-right
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1),  # diagonal up-left
        (1, -1),  # diagonal down-left
    ]

    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for dx, dy in directions:
                x, y = i, j
                word = ""
                visited = set()  # Track visited cells to avoid double-counting
                while (
                    0 <= x < len(grid)
                    and 0 <= y < len(grid[0])
                    and (x, y) not in visited
                ):
                    word += grid[x][y]
                    visited.add((x, y))
                    if pattern in word:
                        if word.startswith(pattern):
                            count += 1
                            break
                    x += dx
                    y += dy

    return count


if __name__ == "__main__":
    filename = "input/day_four_input.txt"
    search_word = "XMAS"
    match_count = find_xmas_count(filename, search_word)
    print(f"Found '{search_word}' {match_count} times in the file!")
