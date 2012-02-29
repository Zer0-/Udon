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
        self.objects.append(something)

    def draw(self):
        for i in self.objects:
            i.draw()

def init():
    global renderstack
    init_window()
    renderstack = RenderStack()
    init_objects()
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

#test method, to be deleted
def init_objects():
    label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=12,
                          x=3, y=window.height-12-3)
    renderstack.add(label)
    dprint("added new label to renderstack")

#The main rendering function (not to be confused with the main loop)
#This will only handle the graphics!
def draw():
    window.clear()
    renderstack.draw()
