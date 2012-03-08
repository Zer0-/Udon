import pyglet
import vectors
from config import DEBUG
from _debug import dprint
import render

class TileGrid:
    """
    Representation of a square grid of tiles. It keeps track of the viewport
    position and renders the visible tiles.

    """
    def __init__(self, viewDimensions, tilemap):
        #the tilemap object is where we go to get our sprites
        self.tilemap = tilemap
        self.scalefactor = 1
        self.tileDimensions = tilemap.tileDimensions #in pixels
        self.mapDimensions = self.getMapDimensions(tilemap.mapDimensions)
        print self.mapDimensions
        self.viewDimensions = viewDimensions
        #view position relative to the top-left corner of the grid. In pixels.
        self.viewPosition = [0, int(tilemap.mapDimensions[0]/2)*self.tileDimensions[1]]
        self.rowshift = self.getRowShiftFn()
        self.positionlabel = self.init_label()

    def init_label(self):
        self.positionlabel =  pyglet.text.Label('',
                          font_name='Times New Roman',
                          font_size=12,
                          x=0, y=render.window.height-12-3)
        render.renderstack.add(self.positionlabel)
        return self.positionlabel

    def scale(self, factor):
        """Zoom in or zoom out"""

        #A float scale factor creates some small issues when rendering sprites
        #(its not pixel-perfectly aligned) which is fine for when you're zoomed
        #out but we want it to be clean at normal zoom level so we change the 
        #float to an integer and the tiles align perfecly again!
        if abs(factor) < 0.0001:
            factor = 0.1

        if (abs(factor - 1) < 0.01):
            factor = 1

        self.scalefactor = factor
        print self.scalefactor

    def getTileDimensions(self):
        return vectors.byscalar(self.scalefactor, self.tileDimensions)

    def getRowShiftFn(self):
        """
        The way the map pixels are mapped to tiles, we need the corner to be
        the left-most tile, so whatever row it falls under (even or odd) will NOT be 
        shifted.
        """
        
        def even(n, row):
            return (n - n*(row % 2))

        def odd(n, row):
            return n*(row % 2)

        if self.tilemap.mapDimensions[0] % 2:
            return even
        else:
            return odd

    #bad name
    def getMapDimensions(self, mapDimensions):
        """
        The size of the grid needed (in tile numbers, not pixels) to render
        the whole map.
        """
        w, h = mapDimensions
        x = w + h
        return (x, x)

    def move_view(self, dx, dy):
        """move the view ("camera") over by specified number of pixels"""
        vectors.addref(self.viewPosition, [-dx, dy])

    def move_view_to_position(self, newp):
        """move the view to (newx, newy)"""
        self.viewPosition = newp

    def draw(self):
        """Draws all visible tiles"""
        def adjustForStupidWindowCoordinates(y):
            return render.window.height - tileheight - y

        tilewidth, tileheight = self.getTileDimensions()
        visiblearea = self.get_visible_area()
        if visiblearea == None:
            return

        xvisible, yvisible = visiblearea
        for y in range(yvisible[0], yvisible[1]+1):
            #we need to move the tiles over (because they aren't squares)
            #to render them properly.
            shift = self.rowshift((tilewidth/2), y)

            for x in range(xvisible[0], xvisible[1]+1):
                #tilemap gets us the correct sprite based on our coordinates.
                sprite = self.tilemap.getSprite(x + self.rowshift(0.5, y), y)
                if not sprite:
                    continue
                #*wrto == "with respect to"
                spritePosX_wrto_map = (x*tilewidth) + shift
                spritePosY_wrto_map = y*(tileheight/2)
                spritePosInWindow = vectors.subtract(
                        [spritePosX_wrto_map, spritePosY_wrto_map],
                        self.viewPosition
                )
                spritePosInWindow[1] = adjustForStupidWindowCoordinates(spritePosInWindow[1])
                sprite.set_position(spritePosInWindow[0], spritePosInWindow[1])
                sprite.scale = self.scalefactor
                sprite.draw()

    def get_visible_area(self):
        """Gets the coordinates of the first and last tiles
           to be visible and rendered by the viewport"""

        viewx, viewy = self.viewPosition
        self.positionlabel.text = str((viewx, viewy))
        viewsizex, viewsizey = self.viewDimensions
        tilewidth, tileheight = self.getTileDimensions()
        tilewidth = int(tilewidth)
        tileheight = int(tileheight)

        #first we should check if we're
        # too far back from the entire map to see anything
        if viewx + viewsizex < 0 or viewy + viewsizey < 0:
            dprint("the view is too far above/left of the field to see anything")
            return None

        #first, last tile indices to be visible in the viewport
        if viewx < tilewidth:
            firstVisibleHorizontally = 0
        else:
            firstVisibleHorizontally = (viewx / tilewidth) - 1

        if viewy < tileheight:
            firstVisibleVertically = 0
        else:
            firstVisibleVertically = (viewy*2 / (tileheight)) - 1

        #now we check if we've overshot the field completely
        if firstVisibleHorizontally > self.mapDimensions[0] \
                or firstVisibleVertically > self.mapDimensions[1]:
            dprint("You've overshot the field (too far down/right) to see anything")
            return None

        lastVisibleHorizontally = ((viewx + viewsizex) / tilewidth)
        lastVisibleVertically = (viewy + viewsizey) / (tileheight/2)
        #what if the map isn't even that big?
        if lastVisibleHorizontally > self.mapDimensions[0]:
            lastVisibleHorizontally = self.mapDimensions[0]

        if lastVisibleVertically > self.mapDimensions[1]:
            lastVisibleVertically = self.mapDimensions[1]

        return (
            (firstVisibleHorizontally, lastVisibleHorizontally),
            (firstVisibleVertically, lastVisibleVertically)
        )
        
