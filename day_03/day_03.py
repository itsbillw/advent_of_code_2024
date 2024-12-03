import re

input_filename = "input/day_three_input.txt"

# Regular expression patterns matching "mul(X,Y)" and "do()" or "don't()"
mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
control_pattern = r"(do\(\)|don't\(\))"

running_total = 0

is_enabled = True  # enable mul instructions by default

with open(input_filename, "r") as file:
    content = file.read()

tokens = re.split(r"(?<=\))", content)

for token in tokens:
    control_match = re.search(control_pattern, token)
    if control_match:
        if control_match.group() == "do()":
            is_enabled = True
        elif control_match.group() == "don't()":
            is_enabled = False
        continue

    mul_match = re.search(mul_pattern, token)
    if mul_match and is_enabled:
        x, y = map(int, mul_match.groups())
        running_total += x * y

print(running_total)
