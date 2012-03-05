import pyglet
import config
from _debug import dprint

#should we have global variables like this?
window = None
renderstack = None

class RenderStack:
    """ For now this is just a set of objects with a .draw method """
    def __init__(self):
        self.objects = []

    def add(self, something):
        self.objects.insert(0, something)

    def draw(self):
        for i in self.objects:
            i.draw()

def init():
    global renderstack
    init_window()
    renderstack = RenderStack()
    init_events()

def init_events():
    window.on_draw = draw

def init_window():
    global window
    w, h = config.WINDOW_RESOLUTION
    dprint("Initializing window")
    dprint("Window resolution:", config.WINDOW_RESOLUTION)
    window = pyglet.window.Window(width=w,
                                  height=h,
                                  caption="Udon",
                                  vsync=config.VSYNC
                                  )

#The main rendering function (not to be confused with the main loop)
#This will only handle the graphics!
def draw():
    window.clear()
    renderstack.draw()
