import pyglet
import config
from _debugprint import dprint

def initWindow():
    w, h = config.WINDOW_RESOLUTION
    dprint("Initializing window")
    dprint("Window resolution:", config.WINDOW_RESOLUTION)
    window = pyglet.window.Window(width=w,
                                  height=h,
                                  caption="Udon"
                                  )
