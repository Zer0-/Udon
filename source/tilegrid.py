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
        #the following variables all have units in pixels
        self.gridDimensions = [
            tilemap.mapDimensions[0] * tilemap.tileDimensions[0],
            tilemap.mapDimensions[1] * tilemap.tileDimensions[1]
        ]
        self.tileDimensions = tilemap.tileDimensions
        self.viewDimensions = viewDimensions
        self.viewPosition = [0,0]

    def move_view(self, dx, dy):
        """move the view over by specified number of pixels"""
        vectors.addref(self.viewPosition, [-dx, dy])

    def move_view_to_position(self, newp):
        """move the view to (newx, newy)"""
        self.viewPosition = newp

    #TODO: use batch
    def draw(self):
        """Draws all visible tiles"""
        def adjustForStupidWindowCoordinates(y):
            return render.window.height - self.tileDimensions[1] - y
            
        def is_even(n):
            return n%2 == 0

        tilewidth, tileheight = self.tileDimensions
        visiblearea = self.get_visible_area()
        if visiblearea == None:
            return

        xvisible, yvisible = visiblearea
        for y in range(yvisible[0], yvisible[1]+1):
            shift = 0
            if not is_even(y):
                shift = tilewidth/2

            for x in range(xvisible[0], xvisible[1]+1):
                sprite = self.tilemap.getSprite(x, y)
                #*wrto == "with respect to"
                spritePosX_wrto_map = (x*tilewidth) + shift
                spritePosY_wrto_map = y*(tileheight/2)
                spritePosInWindow = vectors.subtract(
                        [spritePosX_wrto_map, spritePosY_wrto_map],
                        self.viewPosition
                )
                spritePosInWindow[1] = adjustForStupidWindowCoordinates(spritePosInWindow[1])
                sprite.set_position(spritePosInWindow[0], spritePosInWindow[1])
                sprite.draw()

    def get_visible_area(self):
        """Gets the coordinates of the first and last tiles
           to be visible by the viewport"""

        viewx, viewy = self.viewPosition
        #print viewx, viewy
        viewsizex, viewsizey = self.viewDimensions
        tilewidth, tileheight = self.tileDimensions
        #Using floats here rather than ints will screw up the calculation
        if DEBUG:
            for i in [viewx, viewy, tilewidth, tileheight]:
                if type(i) is not int:
                    print "Warning: In get_visible_area something is a float"

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
        if firstVisibleHorizontally > self.tilemap.mapDimensions[0] \
                or firstVisibleVertically > self.tilemap.mapDimensions[1]:
            dprint("You've overshot the field (too far down/right) to see anything")
            return None

        lastVisibleHorizontally = ((viewx + viewsizex) / tilewidth)
        lastVisibleVertically = (viewy + viewsizey) / (tileheight/2)
        #what if the map isn't even that big?
        if lastVisibleHorizontally > self.tilemap.mapDimensions[0]:
            lastVisibleHorizontally = self.tilemap.mapDimensions[0]

        if lastVisibleVertically > self.tilemap.mapDimensions[1]:
            lastVisibleVertically = self.tilemap.mapDimensions[1]

        return (
            (firstVisibleHorizontally, lastVisibleHorizontally),
            (firstVisibleVertically, lastVisibleVertically)
        )
        
