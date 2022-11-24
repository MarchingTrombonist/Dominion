import os
import bs4
import requests
import pandas as pd
import html5lib


def makeDataFrame(url="http://wiki.dominionstrategy.com/index.php/List_of_cards"):
    dfs = pd.read_html(io=url, flavor="bs4")
    return dfs[0]


# MAKE FOLDERS
def makeFolders(df, cols=["Set"], file_path="\Sets\\"):
    for col in cols:
        for val in df[col].unique():
            full_path = (
                "D:\Comp Sci\Coding\Python\Dominion" + file_path + str(val) + "\\"
            )
            if not os.path.exists(full_path):
                os.makedirs(full_path)


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
