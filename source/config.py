#This is the main configuration file
#All command line args passed to the app
#Will simply modify the settings here on application init


#avoiding absolute paths...
import os
LOCALPATH = os.path.dirname(__file__)


#Begin settings
TEST_MAP = "map1"

MAPS_DIRECTORY = os.path.join(LOCALPATH, "../resources/maps/")
MAP_METADATA_FILENAME = "metadata.json"

DEBUG = True

WINDOW_RESOLUTION = (800, 600) #(width, height)

VSYNC = False
