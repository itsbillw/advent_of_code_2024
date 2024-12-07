import itertools


def evaluate_expression(ops, numbers):
    """
    Evaluate an expression with the given operators and numbers.
    Operators are applied left-to-right without precedence.
    """
    result = numbers[0]
    for op, num in zip(ops, numbers[1:]):
        if op == "+":
            result += num
        elif op == "*":
            result *= num
    return result


def parse_input(filename):
    """
    Parse the input file and return a list of equations.
    Each equation is represented as a tuple: (target_value, numbers).
    """
    equations = []
    with open(filename, "r") as file:
        for line in file:
            if ":" in line:
                target, numbers = line.split(":")
                target = int(target.strip())
                numbers = list(map(int, numbers.split()))
                equations.append((target, numbers))
    return equations


def find_valid_equations(filename):
    """
    Find equations where a combination of + and * operators results in the target value.
    Return the sum of target values for valid equations.
    """
    equations = parse_input(filename)
    valid_sum = 0

    for target, numbers in equations:
        num_ops = len(numbers) - 1
        # Generate all possible operator combinations for the current equation
        for ops in itertools.product(["+", "*"], repeat=num_ops):
            if evaluate_expression(ops, numbers) == target:
                valid_sum += target
                break  # Only count the target value once if it's valid

    return valid_sum


if __name__ == "__main__":
    filename = "input/day_seven_input.txt"
    result = find_valid_equations(filename)
    print(f"Total calibration result: {result}")
