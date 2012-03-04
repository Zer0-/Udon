"""
This module takes events generated by pyglet and 
passes them to the appropriate event handler
"""
import pyglet
class handlers:
    pass

def initEventHandlers(window, maingame):
    handlers.mouseInputHandler = mouseInputHandler(window, maingame)
    handlers.keyboardInputHandler = keyboardInputHandler(window,maingame)
class keyboardInputHandler:
    """Any keyboard related events start to be handled here"""
    def __init__(self, window, maingame):
        self.window = window
        self.game = maingame
        self.register_events()

    def register_events(self):
        self.window.on_key_press = self.on_key_press
        self.window.on_key_release = self.on_key_release
        self.keys = pyglet.window.key.KeyStateHandler()       
        self.window.push_handlers(self.keys)

    def on_key_press(self, symbol, modifiers):
        pass
    def on_key_release(self, symbol, modifiers):
        pass
class mouseInputHandler:
    """Any mouse related events start to be handled here"""
    def __init__(self, window, maingame):
        self.window = window
        self.game = maingame
        self.register_events()

    def register_events(self):
        self.window.on_mouse_press = self.on_mouse_press
        self.window.on_mouse_motion = self.on_mouse_motion
        self.window.on_mouse_drag = self.on_mouse_drag

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        (dx, dy) = (0, 1) -> dragged mouse up
        (dx, dy) = (0, -1) -> dragged mouse down
        (dx, dy) = (1, 0) -> dragged mouse right
        (dx, dy) = (-1, 0) -> dragged mouse left
        """
        self.dragGrid(dx, dy)

    def dragGrid(self, dx, dy):
        self.game.tilegrid.move_view(dx, dy)
