"""
This is a script for creating maps from a folder with a set of images.
Usage:

Create a directory with all your terrain tiles, in isometric view in png format.
Run the script as such:

$            python mapmaker.py -d <path>

where path is the path of the directory you've created.

This will generate three new files in that directory: map.png, metadata.json and pallette.png

map.png:
    This file is the map data for your program. Every pixel corresponds to a tile sprite. You can expand
    and edit this image as needed as long as you are using the initial colors.
    Colors not found in pallette.png will not map to a sprite, therefore that area of the terrain will
    simply be black.

metadata.json:
    This file contains the colors -> filename map for looking up tiles from map.png. As well as the map
    name and other relevant data.

pallette.png:
    This file is not used by the game, it contains a pallette all the colors you can use to edit map.png

"""

import os
import argparse

from PIL import Image
from PIL import ImageEnhance

from random import randrange

class config:
    """Configuration settings for this module"""
    TILESET_DIRECTORY = ""
    QUIET = False

"""metadata for the map that will be generated"""
settings = {
    'map_name': None,
    'colormap': None,
    'tile_dimensions': None
}

def createParser():
    parser = argparse.ArgumentParser(description='Tool for generating maps from set of tile images')
    parser.add_argument("-d", required=True, help="Directory with image files")
    return parser

def processArgs(args):
    if args.d:
        config.TILESET_DIRECTORY = args.d

def openallimages():
    images = []
    names = []
    for i in os.listdir(config.TILESET_DIRECTORY):
        fileName, fileExtension = os.path.splitext(i)
        if fileExtension in ['.png']:
            names.append(i)
            im = Image.open(os.path.join(config.TILESET_DIRECTORY, i))
            images.append(im)

    return (names, images)

def getWidthHeight(images):
    wh = []
    for i in images:
        wh.append(i.size)
    return mostCommon(wh)

def mostCommon(ls):
    """Return the most common element in a list"""
    d = {}
    for i in ls:
        d[i] = d[i]+1 if i in d else 1
    m = dict((v,k) for k, v in d.iteritems())
    return m[max(m.keys())]

def askconfirm(default, statement):
    def yesno():
        s = """%s is "%s" (Yes/No)? """ % (statement, value)
        yn = raw_input(s).lower()
        return yn

    value = default
    yn = yesno()
    print yn
    while yn != "y" and yn != "yes":
        value = raw_input("Enter new value for %s: " % statement)
        yn = yesno()

    return value

def getTileColor(image):
    color = []
    for i in range(3):
        color.append(randrange(255))
    return tuple(color)

#Does not work very well - colors come out way too similar
def getTileColor_OLD(image):
    enh = ImageEnhance.Contrast(image)
    im = enh.enhance(3)
    #bri = ImageEnhance.Brightness(im)
    #im = bri.enhance(3)
    ravg = 0
    gavg = 0
    bavg = 0
    data = im.getdata()
    length = len(data)
    for r, g, b, a in data:
        if a != 0:
            ravg += r
            bavg += b
            gavg += g

    color = []
    for i in [ravg, gavg, bavg]:
        color.append(i/length)

    return tuple(color)

def createmap(names, imgs):
    d = {}
    for i in range(len(names)):
        color = getTileColor(imgs[i])
        while color in d.values():
            color = getTileColor(imgs[i])
        d[names[i]] = color
    return d

def createPallette(d):
    l = len(d.keys())
    im = Image.new("RGB", (l, 1))
    for i in range(l):
        im.putpixel((i, 0), d.values()[i])

    im.save(os.path.join(config.TILESET_DIRECTORY, "pallette.png"),"PNG")
    mapimage = Image.new("RGB", (32,64))
    mapimage.paste(im, (0, 0, im.size[0], im.size[1]))
    mapimage.save(os.path.join(config.TILESET_DIRECTORY, "map.png"),"PNG")

def writemetadata():
    import json
    js = json.dumps(settings, sort_keys=True, indent=4)
    fname = os.path.join(config.TILESET_DIRECTORY, "metadata.json")
    with open(fname, 'w') as f:
        f.write(js)

def main():
    processArgs(createParser().parse_args())
    print "Making map from %s directory" % config.TILESET_DIRECTORY
    map_dirname = os.path.basename(os.path.dirname(config.TILESET_DIRECTORY))
    name = askconfirm(map_dirname, "map name")
    names, imgs = openallimages()
    width, height = getWidthHeight(imgs)
    width = askconfirm(width, "tile width (in pixels)")
    height = askconfirm(height, "tile height (in pixels)")
    colormap = createmap(names, imgs)
    createPallette(colormap)
    settings['map_name'] = name
    settings['colormap'] = colormap
    settings['tile_dimensions'] = tuple([width, height])
    writemetadata()

if __name__ == "__main__":
    main()
