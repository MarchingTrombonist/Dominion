import os
import cardPuller as pull
import time

start_time = time.perf_counter()
# TODO: add separate runner files for dataframe work vs request work

listFile = "Data\\List.csv"

if os.path.exists(listFile):
    df = pull.makeDataFrame(listFile, "csv")
else:
    df = pull.makeDataFrame()
    df.to_csv(listFile, index_label=False)

df = pull.fixMultipleTypes(df)
df = pull.fixSets(df, drop_old=True)

pull.makeFolders(df, True)
pull.pullImages(df, True, False)
pull.makeDecks(df, True)

end_time = time.perf_counter()
print("Time taken: %4.4f seconds" % (end_time - start_time))
