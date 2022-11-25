import os
import bs4
import requests
import pandas as pd
import numpy as np


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
    df = df.drop(columns=["Types"])
    df.insert(1, "Type Four", dfSplit[3])
    df.insert(1, "Type Three", dfSplit[2])
    df.insert(1, "Type Two", dfSplit[1])
    df.insert(1, "Type One", dfSplit[0])
    return df


def fixSets(df, drop_old=False):
    dfSplit = df["Set"].str.split(", ", expand=True)
    df = df.drop(columns=["Set"])
    df.insert(1, "Edition", dfSplit[1])
    df.insert(1, "Set", dfSplit[0])
    if drop_old:
        df = df.drop(df[df["Edition"] == "1E"].index)
        df = df.drop(columns=["Edition"])
        df = df.reset_index()
    return df


# TODO: add bs4 ["COST"] processing to get values


# MAKE FOLDERS
# TODO: Add nested folders: set\type\card
# TODO: Add nested folders: type\set\card
def makeFolders(df):
    unique_list = df["Set"].unique()
    for set in unique_list:
        print(
            "Creating %s folder [%d/%d]"
            % (set, np.where(unique_list == set)[0][0] + 1, len(unique_list)),
            end="",
        )
        full_path = "D:\\Comp Sci\\Coding\\Python\\Dominion\\Sets\\" + str(set) + "\\"
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(" \u2713")
        print("DONE")


# GET IMAGE
# Loops through card data and requests image file; saves to folder
# TODO: Multithreading?
def pullImages(df, print_cards=False):
    for ind in df.index:
        card_name = df["Name"][ind]
        card_set = df["Set"][ind]
        # card_type = card[2]
        card_path = "Sets\\" + card_set + "\\" + card_name + ".jpg"

        if print_cards:
            print(
                "Processing %s's %s [%d/%d]" % (card_set, card_name, ind + 1, len(df)),
                end="",
            )

        if not os.path.exists(card_path):
            html = requests.get(
                "http://wiki.dominionstrategy.com/index.php/File:" + card_name + ".jpg"
            ).text
            site = bs4.BeautifulSoup(html, "html.parser")
            if print_cards:
                print(" \u2713", end="")

            image_link = site.find("div", class_="fullImageLink").a.img.get("src")
            if print_cards:
                print(" \u2713", end="")

            image = requests.get(
                "http://wiki.dominionstrategy.com" + image_link
            ).content
            if print_cards:
                print(" \u2713", end="")

            f = open("Sets\\" + card_set + "\\" + card_name + ".jpg", "wb+")
            f.write(image)
            f.close
            if print_cards:
                print(" \u2713", end="")

        if print_cards:
            print(" DONE")
