import re

input_filename = "input/day_three_input.txt"

# Regular expression pattern to match "mul(X,Y)"
pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

running_total = 0

# Read and process the file
with open(input_filename, "r") as file:
    content = file.read()

matches = re.findall(pattern, content)

running_total = sum(int(x) * int(y) for x, y in matches)

print(running_total)
