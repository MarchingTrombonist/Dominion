import cardPuller as pull

df = pull.makeDataFrame()
df = pull.fixMultipleTypes(df)
print(df)
# pull.makeFolders(df, cols=["Types"], file_path="\pdTest\\")
# pull.displayDataFrame(df)
