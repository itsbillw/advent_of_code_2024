import pandas as pd

df = pd.read_csv(
    "input/day_two_input.txt",
    sep=" ",
    header=None,
)


def row_safety_check(row):
    status_check = "Safe"
    check_direction = []
    check_gap = []
    check_value = None

    for value in row:
        if pd.isna(value):  # Skip NaN values
            continue
        if check_value is None:
            check_value = value
        else:
            gap = abs(value - check_value)
            check_gap.append(gap)

            if check_value > value:
                check_direction.append("DESC")
            else:
                check_direction.append("ASC")

            check_value = value

    if not all(1 <= gap <= 3 for gap in check_gap):
        status_check = "Unsafe"

    unique_directions = set(check_direction)
    if len(unique_directions) > 1:
        status_check = "Unsafe"

    return status_check


df["Status"] = df.apply(row_safety_check, axis=1)

print(df[df["Status"] == "Safe"])
