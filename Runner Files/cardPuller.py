import os
import bs4
import requests
import pandas as pd
import numpy as np
import _thread


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


# TODO: pull deck quantities and add to df
def getCardQuant(df):
    return


# TODO: add bs4 ["COST"] processing to get values


# MAKE FOLDERS
# TODO: Add nested folders: set\type\card
# TODO: Add nested folders: type\set\card
def makeFolders(df, print_tracking=False):
    unique_list = df["Set"].unique()
    for set in unique_list:
        if print_tracking:
            print(
                "Creating %s folder [%d/%d]"
                % (set, np.where(unique_list == set)[0][0] + 1, len(unique_list)),
                end="",
            )

        card_path = (
            "D:\\Comp Sci\\Coding\\Python\\Dominion\\Sets\\" + str(set) + "\\Cards\\"
        )
        deck_path = (
            "D:\\Comp Sci\\Coding\\Python\\Dominion\\Sets\\" + str(set) + "\\Decks\\"
        )
        if not os.path.exists(card_path):
            os.makedirs(card_path)

            if print_tracking:
                print(" \u2713", end="")

        if not os.path.exists(deck_path):
            os.makedirs(deck_path)

            if print_tracking:
                print(" \u2713", end="")

        if print_tracking:
            print("DONE")


# GET IMAGE
# Loops through card data and requests image file; saves to folder
# TODO: Multithreading? https://stackoverflow.com/questions/38280094/python-requests-with-multithreading
def pullImages(df, print_tracking=False, m_thread=False):
    for ind in df.index:
        if m_thread:
            try:
                _thread.start_new_thread(threadPullImages, (ind, df, True))
            except:
                print("Error")
        else:
            card_name = df["Name"][ind]
            card_set = df["Set"][ind]
            # card_type = card[2]
            card_path = "Sets\\" + card_set + "\\Cards\\" + card_name + ".jpg"

            if print_tracking:
                print(
                    "Processing %s's %s [%d/%d]"
                    % (card_set, card_name, ind + 1, len(df)),
                    end="",
                )

            if not os.path.exists(card_path):
                html = requests.get(
                    "http://wiki.dominionstrategy.com/index.php/File:"
                    + card_name
                    + ".jpg"
                ).text
                site = bs4.BeautifulSoup(html, "html.parser")
                if print_tracking:
                    print(" \u2713", end="")

                image_link = site.find("div", class_="fullImageLink").a.img.get("src")
                if print_tracking:
                    print(" \u2713", end="")

                image = requests.get(
                    "http://wiki.dominionstrategy.com" + image_link
                ).content
                if print_tracking:
                    print(" \u2713", end="")

                f = open(card_path, "wb+")
                f.write(image)
                f.close
                if print_tracking:
                    print(" \u2713", end="")

            if print_tracking:
                print(" DONE")


# TODO: Make .jpg image grids instead of .tsdb files
# (https://stackoverflow.com/questions/4567409/python-image-library-how-to-combine-4-images-into-a-2-x-2-grid)
# TODO: Write directly to saved game??
# Put into saved objects vs spawned on table
# Maybe spawn non-supply cards?
# ("C:\Users\macal\OneDrive\Documents\My Games\Tabletop Simulator\Saves\TS_Save_1.json")
def makeDecks(df, print_tracking=False):
    for ind in df.index:
        card_name = df["Name"][ind]
        card_set = df["Set"][ind]
        # card_type = card[2]
        card_path = "Sets\\" + card_set + "\\Cards\\" + card_name + ".jpg"
        deck_path = "Sets\\" + card_set + "\\Decks\\" + card_name + ".tsdb"

        if print_tracking:
            print(
                "Forming %s's %s into a deck [%d/%d]"
                % (card_set, card_name, ind + 1, len(df)),
                end="",
            )

        if not os.path.exists(deck_path):
            # TODO: Get deck quant
            # html = requests.get(
            #     "http://wiki.dominionstrategy.com/index.php/File:"
            #     + card_name
            #     + ".jpg"
            # ).text
            # site = bs4.BeautifulSoup(html, "html.parser")
            # if print_tracking:
            #     print(" \u2713", end="")

            # image_link = site.find("div", class_="fullImageLink").a.img.get("src")
            # if print_tracking:
            #     print(" \u2713", end="")

            # image = requests.get(
            #     "http://wiki.dominionstrategy.com" + image_link
            # ).content
            # if print_tracking:
            #     print(" \u2713", end="")

            f = open(deck_path, "w")
            f.write(
                """
# Save File
cardsx=5
cardsy=2
card-width=375
card-height=599
zoom=0.3
background-color=-16777216
0_0=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
1_0=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
2_0=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
3_0=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
4_0=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
0_1=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
1_1=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
2_1=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
3_1=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
4_1=D\:\\Comp Sci\\Coding\\Python\\Dominion\\{0}
""".format(
                    card_path
                )
            )
            f.close
            if print_tracking:
                print(" \u2713", end="")

        if print_tracking:
            print(" DONE")


def threadPullImages(ind, df, print_cards=False):
    card_name = df["Name"][ind]
    card_set = df["Set"][ind]
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

        image = requests.get("http://wiki.dominionstrategy.com" + image_link).content
        if print_cards:
            print(" \u2713", end="")

        f = open("Sets\\" + card_set + "\\" + card_name + ".jpg", "wb+")
        f.write(image)
        f.close
        if print_cards:
            print(" \u2713", end="")

    if print_cards:
        print(" DONE")
