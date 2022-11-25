import os
import bs4
import requests
import pandas as pd
import html5lib
import re


def makeDataFrame(
    src="http://wiki.dominionstrategy.com/index.php/List_of_cards", type="html"
):
    if type == "html":
        dfs = pd.read_html(io=src, flavor="bs4")
        return dfs[0]
    elif type == "csv":
        df = pd.read_csv(src)
        return df
    else:
        raise ValueError


def fixMultipleTypes(df):
    dfSplit = df["Types"].str.split(" - ", expand=True)
    df.drop(columns=["Types"], inplace=True)
    df.insert(1, "Type Four", dfSplit[3])
    df.insert(1, "Type Three", dfSplit[2])
    df.insert(1, "Type Two", dfSplit[1])
    df.insert(1, "Type One", dfSplit[0])
    return df


def fixSets(df):
    dfSplit = df["Set"].str.split(", ", expand=True)
    df.drop(columns=["Set"], inplace=True)
    df.insert(1, "Edition", dfSplit[1])
    df.insert(1, "Set", dfSplit[0])
    df["Edition"].replace("None", "1E")
    return df


# TODO: add bs4 ["COST"] processing to get values


# MAKE FOLDERS
# TODO: Add nested folders: set\type\card
# TODO: Add nested folders: type\set\card
def makeFolders(df, file_path="\Sets\\"):
    for set in df["Set"].unique():
        full_path = "D:\Comp Sci\Coding\Python\Dominion" + str(set) + "\\"
        if not os.path.exists(full_path):
            os.makedirs(full_path)


# GET IMAGE
# Loops through card data and requests image file; saves to folder
def pullImages(df, print=False):
    for card in df:
        card_name = card[0]
        card_set = card[1]
        # card_type = card[2]

        print("Processing %s's %s" % (card_set, card_name), end="")

        html = requests.get(
            "http://wiki.dominionstrategy.com/index.php/File:" + card_name + ".jpg"
        ).text
        site = bs4.BeautifulSoup(html, "html.parser")

        image_link = site.find("div", class_="fullImageLink").a.img.get("src")
        image = requests.get("http://wiki.dominionstrategy.com" + image_link).content
        f = open("Sets\\" + card_set + "\\" + card_name + ".jpg", "wb+")
        f.write(image)
        f.close

        print("\u2713")
