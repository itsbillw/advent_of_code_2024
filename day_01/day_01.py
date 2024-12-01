import pandas as pd

df = pd.read_csv("day_one_input.txt", sep=" ", index_col=None, header=None, usecols=[0,3], names=["List1", "List2"])

df['List1'] = df['List1'].sort_values().reset_index(drop=True)
df['List2'] = df['List2'].sort_values().reset_index(drop=True)

df["Distance"] = abs(df["List1"] - df["List2"])

print(df["Distance"].sum())
