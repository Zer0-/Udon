import render
import pyglet

import config
import tilegrid
import tilemap
import userinput

"""
A disclaimer:
From the pyglet docs:
"To write 3D applications or achieve optimal performance in your 2D applications you'll need to work with OpenGL directly"
I'm not going to use this. Someone with more knowlege than me can modify
the code to use opengl. For now I will just get things up and running.
"""

class maingame:
    """
    The top level class for the game. For now it only displays the current fps
    """
    def __init__(self):
        self.fpslabel = pyglet.text.Label('',
                          font_name='Times New Roman',
                          font_size=12,
                          x=render.window.width-50, y=render.window.height-12-3)

        self.tilegrid = tilegrid.TileGrid(config.WINDOW_RESOLUTION, tilemap.TileMap())
        render.renderstack.add(self.fpslabel)
        render.renderstack.add(self.tilegrid)

    def this_is_where_it_all_begins(self, dt):
            self.fpslabel.text = "%.2f" % pyglet.clock.get_fps()

if __name__ == "__main__":
    render.init()
    m = maingame()
    userinput.initEventHandlers(render.window, m)
    pyglet.clock.set_fps_limit(30)
    pyglet.clock.schedule(m.this_is_where_it_all_begins)
    pyglet.app.run()
