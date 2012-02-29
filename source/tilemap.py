import pyglet
import config

class TileMap:
    def __init__(self):
        image = pyglet.image.load(config.TEST_TILE)
        self.tileDimensions = (image.width, image.height)
        self.mapDimensions = (300, 300)
        self.sprite = pyglet.sprite.Sprite(image)

    def getSprite(self, x, y):
        return self.sprite
