import os
import bs4
import requests
import pandas as pd
import html5lib
import re


def makeDataFrame(url="http://wiki.dominionstrategy.com/index.php/List_of_cards"):
    dfs = pd.read_html(io=url, flavor="bs4")
    return dfs[0]


def fixMultipleTypes(df):
    dfSplit = df["Types"].str.split(" - ", expand=True)
    df.insert(2, "Type Four", dfSplit[3])
    df.insert(2, "Type Three", dfSplit[2])
    df.insert(2, "Type Two", dfSplit[1])
    df.insert(2, "Type One", dfSplit[0])
    df.drop(columns=["Types"], inplace=True)
    return df


# TODO: add bs4 ["COST"] processing to get values


# MAKE FOLDERS
# TODO: Add nested folders: set\type\card
# TODO: Add nested folders: type\set\card
def makeFolders(df, cols=["Types"], file_path="\Sets\\"):
    for col in cols:
        for set in df["Set"].unique():
            setDF = df[df["Set"] == set]
            print(setDF[col].unique())
            for val in setDF[col].unique():
                full_path = (
                    "D:\Comp Sci\Coding\Python\Dominion"
                    + file_path
                    + "\\"
                    + set
                    + "\\"
                    + str(val)
                    + "\\"
                )
                if not os.path.exists(full_path):
                    os.makedirs(full_path)


# GET IMAGE
# Loops through card data and requests image file; saves to folder
def pullImages(df):
    for card in df:
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
