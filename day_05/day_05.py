import pandas as pd


def load_data(file_path):
    """
    Load the rules and updates from a single file.
    The file is split into two sections separated by a blank line.
    """
    with open(file_path, "r") as file:
        content = file.read().strip().split("\n\n")
        rules_section = content[0].strip()
        updates_section = content[1].strip()

    # Parse rules into a DataFrame
    rules = pd.DataFrame(
        [line.split("|") for line in rules_section.split("\n")],
        columns=["X", "Y"],
    ).astype(int)

    # Parse updates into a list of lists
    updates = [list(map(int, line.split(","))) for line in updates_section.split("\n")]

    return rules, updates


def is_valid_update(rules_df, update):
    """
    Check if the update follows the ordering rules using Pandas.
    """
    update_df = pd.DataFrame({"page": update, "index": range(len(update))})
    # Merge rules with the update dataframe to find relevant constraints
    merged_rules = rules_df.merge(
        update_df,
        left_on="X",
        right_on="page",
        how="inner",
    ).merge(update_df, left_on="Y", right_on="page", how="inner", suffixes=("_X", "_Y"))
    # Check if any rule is violated (i.e., X's index >= Y's index)
    violations = merged_rules["index_X"] >= merged_rules["index_Y"]
    return not violations.any()


def find_middle_page(update):
    """
    Find the middle page of an update.
    """
    return update[len(update) // 2]


def process_updates(file_path):
    """
    Process updates and calculate the sum of middle pages for correctly ordered updates.
    """
    rules_df, updates = load_data(file_path)
    middle_sum = 0

    for update in updates:
        if is_valid_update(rules_df, update):
            middle_sum += find_middle_page(update)

    return middle_sum


# File path
input_file = "input/day_five_input.txt"

# Calculate the result
result = process_updates(input_file)
print(f"Sum of middle pages for correctly ordered updates: {result}")
