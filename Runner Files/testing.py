import pandas as pd

data = {
    "name": ["Sheldon", "Penny", "Amy", "Penny", "Raj", "Sheldon"],
    "year": [[1, 2, 3, 4], 2012, 2013, 2014, 2014, 2012],
    "episodes": [42, 24, 31, 29, 37, 40],
}
df = pd.DataFrame(data, index=["a", "b", "c", "d", "e", "f"])

print(df["year"].unique())
