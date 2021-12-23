import re
from PIL import Image, ImageDraw
import numpy as np
np.seterr(divide = 'ignore')

fileName = "MTL.txt"
imageName = "B4.TIF"
cherkesskCoordinates = {
    "UL": [44.2, 41.9],
    "UR": [44.2, 42.1],
    "LL": [44.2, 42.1],
    "LR": [44.2, 42.0]
}


def getPixels(filename):
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        print(f"{filename} doesn't exist")
        exit(-1)
    text = f.read()
    size = {
        "LINES": float(re.search(r"(?<=THERMAL_LINES = )\d*.\d", text)[0]),
        "SAMPLES": float(re.search(r"(?<=THERMAL_SAMPLES = )\d*.\d", text)[0])
    }
    return size


def getCoord(filename):
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        print(f"{filename} doesn't exist")
        exit(-1)
    text = f.read()
    coordinates = {
        "UL": [float(re.search(r"(?<=CORNER_UL_LAT_PRODUCT = )\d*.\d", text)[0]),
               float(re.search(r"(?<=CORNER_UL_LON_PRODUCT = )\d*.\d", text)[0])],
        "UR": [float(re.search(r"(?<=CORNER_UR_LAT_PRODUCT = )\d*.\d", text)[0]),
               float(re.search(r"(?<=CORNER_UR_LON_PRODUCT = )\d*.\d", text)[0])],
        "LL": [float(re.search(r"(?<=CORNER_LL_LAT_PRODUCT = )\d*.\d", text)[0]),
               float(re.search(r"(?<=CORNER_LL_LON_PRODUCT = )\d*.\d", text)[0])],
        "LR": [float(re.search(r"(?<=CORNER_LR_LAT_PRODUCT = )\d*.\d", text)[0]),
               float(re.search(r"(?<=CORNER_LR_LON_PRODUCT = )\d*.\d", text)[0])]
    }
    f.close()
    return coordinates


def deltaCoords(filename, deltas):
    coordinates = getCoord(filename)
    coords = {
        "UL": [],
        "UR": [],
        "LL": [],
        "LR": []
    }
    for coordinate in coordinates:
        coords[coordinate].append(
            abs((coordinates[coordinate][0] - cherkesskCoordinates[coordinate][0]) * deltas["height"]))
        coords[coordinate].append(
            abs((coordinates[coordinate][1] - cherkesskCoordinates[coordinate][1]) * deltas["width"]))

    return coords


def deltaPixel(height, width, coordinates):
    deltas = {
        "width": height / (coordinates["UR"][1] - coordinates["UL"][1]),
        "height": width / (coordinates["UR"][0] - coordinates["LR"][0])}
    return deltas


def newImage(name, newImageName, newPixels, height):
    try:
        image = Image.open(name)
    except FileNotFoundError:
        print(f"Image doesn't exist, {name} is incorrect. Can't crop it")
        exit(-1)
    width = 8151
    cropped = image.crop((newPixels["UL"][1] , height - newPixels["LL"][0], width - newPixels["UR"][1] - 600, newPixels["UR"][0]))
    cropped.save(newImageName)
    print(image.size)
    image = Image.open("b2_cut.TIF")
    print(image.size)

pixel = getPixels(fileName)
delta = deltaPixel(pixel["LINES"], pixel["SAMPLES"], getCoord(fileName))
pixels = deltaCoords(fileName, delta)
print(delta)
print(pixel)
print(pixels)
newImage(imageName, "b4_cut.TIF", pixels, pixel["LINES"])

image_tiff3 = Image.open('b3_cut.TIF')
image_tiff4 = Image.open('b4_cut.TIF')
red = np.array(image_tiff3).astype(np.int)
nir = np.array(image_tiff4).astype(np.int)
# print('red', red)
# print('nir', nir)
# print(len(red))
# print(len(nir))
ndvi = []
ndvi = ((nir-red)/(nir+red))
print(ndvi)
# print(image_tiff4.getpixel((400, 400)))
# print(image_tiff3.getpixel((400, 400)))
ndvi_new = Image.new('RGB', image_tiff3.size, color=(255, 255, 255))
row = 0
for i in ndvi:
    for num in range(len(i)):
        if 0.91-0.12 <= i[num] <= 1-0.12:
            ndvi_new.putpixel((num, row), (4, 18, 14))
        elif 0.81-0.12 <= i[num] <= 0.9-0.12:
            ndvi_new.putpixel((num, row), (4, 42, 4))
        elif 0.71-0.12 <= i[num] <= 0.8-0.12:
            ndvi_new.putpixel((num, row), (4, 58, 4))
        elif 0.61-0.12 <= i[num] <= 0.7-0.12:
            ndvi_new.putpixel((num, row), (4, 74, 4))
        elif 0.51-0.12 <= i[num] <= 0.6-0.12:
            ndvi_new.putpixel((num, row), (4, 98, 4))
        elif 0.46-0.12 <= i[num] <= 0.5-0.12:
            ndvi_new.putpixel((num, row), (28, 114, 4))
        elif 0.4-0.12 <= i[num] <= 0.4599999-0.12:
            ndvi_new.putpixel((num, row), (60, 134, 4))
        elif 0.36-0.12 <= i[num] <= 0.399999-0.12:
            ndvi_new.putpixel((num, row), (84, 150, 4))
        elif 0.3-0.12 <= i[num] <= 0.3599999-0.12:
            ndvi_new.putpixel((num, row), (100, 162, 4))
        elif 0.26-0.12 <= i[num] <= 0.299999-0.12:
            ndvi_new.putpixel((num, row), (116, 170, 4))
        elif 0.2-0.12 <= i[num] <= 0.2599-0.12:
            ndvi_new.putpixel((num, row), (148, 182, 20))
        elif 0.166-0.12 <= i[num] <= 0.1999-0.12:
            ndvi_new.putpixel((num, row), (124, 158, 4))
        elif 0.133-0.12 <= i[num] <= 0.1665-0.12:
            ndvi_new.putpixel((num, row), (148, 114, 60))
        elif 0.1-0.12 <= i[num] <= 0.1332-0.12:
            ndvi_new.putpixel((num, row), (164, 130, 76))
        elif 0.066-0.12 <= i[num] <= 0.099-0.12:
            ndvi_new.putpixel((num, row), (180, 150, 108))
        elif 0.033-0.12 <= i[num] <= 0.065-0.12:
            ndvi_new.putpixel((num, row), (196, 186, 164))
        elif 0-0.12 <= i[num] <= 0.032-0.12:
            ndvi_new.putpixel((num, row), (252, 254, 252))
        elif i[num] >= -1-0.12:
            ndvi_new.putpixel((num, row), (4, 18, 60))
    row += 1

ndvi_new.show()
