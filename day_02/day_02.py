import pandas as pd

df = pd.read_csv(
    "input/day_two_input.txt",
    sep=" ",
    header=None,
)


def is_safe_with_removal(values):
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

        return gaps_valid and directions_consistent

    for i in range(len(values)):
        modified_row = [v for j, v in enumerate(values) if j != i]
        if row_safety_check(modified_row):
            return "Safe"

    return "Unsafe"


df["Status"] = df.apply(is_safe_with_removal, axis=1)

print(df[df["Status"] == "Safe"])
