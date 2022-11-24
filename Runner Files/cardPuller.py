import os
import bs4
import requests


# Get HTML of wiki card list
CARD_TABLE = bs4.BeautifulSoup(
    requests.get("http://wiki.dominionstrategy.com/index.php/List_of_cards").text,
    "html.parser",
)

# Stores card data
data = []
card = ["START"]

# Loops through html and finds all table rows and pulls data
for row in CARD_TABLE.find_all("tr"):
    for col in row.find_all("td", limit=2):
        tableData = " ".join(col.get_text().split())
        card.append(tableData)

    if card[0].find("v . t . e") != -1:
        break
    data.append(card)
    card = []
data.remove(["START"])


# GET SET LIST
packList = []

for row in data:
    packList.append(row[1])

packList = list(set(packList))


# MAKE FOLDERS
for pack in packList:
    os.makedirs("D:\Comp Sci\Coding\Python\Dominion\Sets\\" + str(pack) + "\\")

# GET IMAGE
# Loops through card data and requests image file; saves to folder
for card in data:
    name = card[0]
    set = card[1]

    html = requests.get(
        "http://wiki.dominionstrategy.com/index.php/File:" + name + ".jpg"
    ).text
    site = bs4.BeautifulSoup(html, "html.parser")

    imageLink = site.find("div", class_="fullImageLink").a.img.get("src")
    image = requests.get("http://wiki.dominionstrategy.com" + imageLink).content
    f = open("Sets\\" + set + "\\" + name + ".jpg", "wb+")
    f.write(image)
    f.close
