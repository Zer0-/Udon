import os
import pyglet
import config
import json
from PIL import Image

class TileMap:
    """
    This class loads the images from a map as sprites.
    It lets the game lookup what kind of tile is at
    a given position. Simply initiate it with a map name
    and it will feed you sprites!
    """
       
    def __init__(self, mapname):
        self.tileDimensions = None
        self.mapDimensions = (0, 0)
        #color to sprite object map
        self.map = {}
        self.mapname = mapname
        #pixel data
        self.mapimage = None
        self.loadmap()

    def getSprite(self, x, y):
        color = self.mapimage[x, y]
        if not color in self.map:
            return None
        return self.map[color]

    def loadsprites(self, folder, meta):
        """ Creates self.map, loads sprites into memory """
        colorFilenamePairs = []
        colormap = meta["colormap"]
        for i in colormap.keys():
            #can remove "tuple" if we have fixed mapmaker to return the colors as tuples
            colorFilenamePairs.append((i, tuple(colormap[i])))

        for i in colorFilenamePairs:
            imagepath = os.path.join(folder, i[0])
            print imagepath
            image = pyglet.image.load(imagepath)
            newsprite = pyglet.sprite.Sprite(image)
            self.map[i[1]] = newsprite

    def loadMapMap(self, filepath):
        """This loads the image file with map data"""
        im = Image.open(filepath)
        import vectors
        self.mapDimensions = vectors.subtract(im.size, (1, 1))
        self.mapimage = im.load()

    def loadmap(self):
        """Finds and gets map information, calls other loading methods"""
        def parseJson(f):
            with open(f, 'r') as fi:
                parsed = json.loads(fi.read())
            return parsed

        def getMapInfo(mapname):
            for d in os.listdir(config.MAPS_DIRECTORY):
                try:
                    folder = os.path.join(config.MAPS_DIRECTORY, d)
                    f = os.path.join(folder, config.MAP_METADATA_FILENAME)
                    meta = parseJson(f)
                except:
                    continue
                if meta["map_name"] == mapname:
                    return meta, folder

            raise Exception("Map %s not found!" % mapname)
                    
        meta, foldername = getMapInfo(self.mapname)
        self.tileDimensions = meta["tile_dimensions"]
        print self.tileDimensions
        self.loadMapMap(os.path.join(foldername, "map.png"))
        self.loadsprites(foldername, meta)
