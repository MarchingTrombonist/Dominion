import os
import bs4
import requests


# Get HTML of wiki card list
def getListHTML():
    LIST_HTML = bs4.BeautifulSoup(
        requests.get("http://wiki.dominionstrategy.com/index.php/List_of_cards").text,
        "html.parser",
    )
    return LIST_HTML


def makeDataTable(LIST_HTML, col_num=3):
    # Stores card data
    data = []
    card = ["START"]

    # Loops through html and finds all table rows and pulls data
    for row in LIST_HTML.find_all("tr"):
        for col in row.find_all("td", limit=col_num):
            table_data = " ".join(col.get_text().split())
            card.append(table_data)

        if card[0].find("v . t . e") != -1:
            break
        data.append(card)
        card = []
    data.remove(["START"])
    return data


# GET PACK/TYPE LIST
def createDataList(data, data_list=[1, 2]):
    data_arr = []
    for val in data_list:
        eval(str(val) + "_list = []")

    for row in data:
        for val in data_list:
            eval(str(val) + "_list.append(row[" + str(val) + "]")

    for val in data_list:
        eval("data_arr.append(" + str(val) + "_list)")

    return data_arr


# MAKE FOLDERS
def makeFolders(data_arr):
    for pack in data_arr[0]:
        os.makedirs("D:\Comp Sci\Coding\Python\Dominion\Sets\\" + str(pack) + "\\")


# GET IMAGE
# Loops through card data and requests image file; saves to folder
def pullImages(data):
    for card in data:
        card_name = card[0]
        card_set = card[1]
        card_type = card[2]

        html = requests.get(
            "http://wiki.dominionstrategy.com/index.php/File:" + card_name + ".jpg"
        ).text
        site = bs4.BeautifulSoup(html, "html.parser")

        image_link = site.find("div", class_="fullImageLink").a.img.get("src")
        image = requests.get("http://wiki.dominionstrategy.com" + image_link).content
        f = open("Sets\\" + card_set + "\\" + card_name + ".jpg", "wb+")
        f.write(image)
        f.close
