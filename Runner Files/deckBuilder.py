import os
from PIL import Image, ImageOps


def imageGrid(card_name, card_set, card_count):
    grid_width = 5
    grid_height = card_count // 5 + (card_count % 5 > 0)
    baseImage = Image.open("Sets\\" + card_set + "\\Cards\\" + card_name + ".jpg")

    imageGrid = Image.new(
        baseImage.mode, [baseImage.width * grid_width, baseImage.height * grid_height]
    )

    for row in range(grid_height):
        for col in range(grid_width):
            offset = baseImage.width * col, baseImage.height * row
            imageGrid.paste(baseImage, offset)

    imageGrid.save("Sets\\" + card_set + "\\Decks\\" + card_name + ".jpg")
    return


imageGrid("Artisan", "Base", 11)
