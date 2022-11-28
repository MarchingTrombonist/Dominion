import cardPuller as pull
import os

listFile = "Data\\List.csv"

if os.path.exists(listFile):
    df = pull.makeDataFrame(listFile, "csv")
else:
    df = pull.makeDataFrame()
    df.to_csv(listFile, index_label=False)

print(df["Types"].unique())
