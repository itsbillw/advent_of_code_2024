import re

input_filename = "input/day_three_input.txt"

file = open(input_filename, "r")

# Checking for pattern "mul(X,Y)" where X and Y are 1-3 digit numbers
pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

running_total = 0

while True:
    content = file.readline()
    matches = re.findall(pattern, content)
    results = [(int(x), int(y)) for x, y in matches]
    for result in results:
        running_total += result[0] * result[1]
    if not content:
        break

file.close()

print(running_total)
