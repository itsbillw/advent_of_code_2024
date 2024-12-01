import pandas as pd

# read input into dataframe
input_file = "input/day_one_input.txt"
df = pd.read_csv(
    input_file,
    sep=" ",
    index_col=None,
    header=None,
    usecols=[0, 3],
    names=["List1", "List2"],
)

# sort values in both columns in ascending order
df["List1"] = df["List1"].sort_values().reset_index(drop=True)
df["List2"] = df["List2"].sort_values().reset_index(drop=True)

# calculate differences between lists
df["Distance"] = abs(df["List1"] - df["List2"])

print("Answer to part one is: ", df["Distance"].sum())

# calculate frequency of value from first column in second column
list2_counts = df["List2"].value_counts()
df["Frequency"] = df["List1"] * df["List1"].map(list2_counts)

print("Answer to part two is: ", df["Frequency"].sum())
