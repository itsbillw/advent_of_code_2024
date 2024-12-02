import pandas as pd

df = pd.read_csv(
    "input/day_two_input.txt",
    sep=" ",
    header=None,
)


def row_safety_check(row):
    check_gap = []
    check_directions = []
    prev_value = None

    for value in row:
        if pd.isna(value):  # Skip NaN values
            continue
        if prev_value is not None:
            gap = abs(value - prev_value)
            check_gap.append(gap)

            direction = "DESC" if prev_value > value else "ASC"
            check_directions.append(direction)

        prev_value = value

    gaps_valid = all(1 <= gap <= 3 for gap in check_gap)
    directions_consistent = len(set(check_directions)) <= 1

    return "Safe" if gaps_valid and directions_consistent else "Unsafe"


df["Status"] = df.apply(row_safety_check, axis=1)

print(df[df["Status"] == "Safe"])
