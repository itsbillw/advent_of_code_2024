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


def reorder_update(rules_df, update):
    """
    Reorder an update based on the ordering rules.
    Perform a topological sort of the pages based on the constraints.
    """
    # Build a dependency graph as adjacency list
    graph = {page: set() for page in update}
    for _, row in rules_df.iterrows():
        if row["X"] in graph and row["Y"] in graph:
            graph[row["Y"]].add(row["X"])

    # Perform topological sort
    sorted_pages = []
    visited = set()
    temp_mark = set()

    def visit(node):
        if node in temp_mark:
            raise ValueError("Cycle detected in rules")
        if node not in visited:
            temp_mark.add(node)
            for predecessor in graph[node]:
                visit(predecessor)
            temp_mark.remove(node)
            visited.add(node)
            sorted_pages.append(node)

    for page in update:
        if page not in visited:
            visit(page)

    # Return sorted list in reverse because we add nodes post-order
    return sorted_pages[::-1]


def find_middle_page(update):
    """
    Find the middle page of an update.
    """
    return update[len(update) // 2]


def process_updates(file_path):
    """
    Process updates, validating and reordering where necessary.
    Calculate the sum of middle pages for both valid and reordered updates.
    """
    rules_df, updates = load_data(file_path)
    middle_sum_valid = 0
    middle_sum_reordered = 0

    for update in updates:
        if is_valid_update(rules_df, update):
            middle_sum_valid += find_middle_page(update)
        else:
            reordered_update = reorder_update(rules_df, update)
            middle_sum_reordered += find_middle_page(reordered_update)

    return middle_sum_valid, middle_sum_reordered


# File path
input_file = "input/day_five_input.txt"

# Calculate the result
valid_sum, reordered_sum = process_updates(input_file)
print(f"Sum of middle pages for correctly ordered updates: {valid_sum}")
print(f"Sum of middle pages for reordered updates: {reordered_sum}")
