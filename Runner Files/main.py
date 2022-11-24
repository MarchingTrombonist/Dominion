import cardPuller as pull

LIST_HTML = pull.getListHTML()
data = pull.makeDataTable(LIST_HTML, 3)
data_arr = pull.createDataList(data, [1, 2])
print(data_arr)
