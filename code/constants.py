import arcade
from arcade.types import LRBT
from pyglet.image import load as pyglet_load
import arcade.gui
import math
import random
import json
import enum
import os

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SCALING = 0.7

COLOR_BACKGROUND = (20, 30, 40, 0)
COLOR_BACKGROUND = (20, 15, 30)
COLOR_PLATFORM = (40, 35, 60)
COLOR_PLATFORM_LIGHT = (60, 55, 90)
COLOR_HIGHLIGHT = (100, 200, 255)
COLOR_UI_TEXT = (240, 240, 200)
COLOR_SELECTED = (255, 215, 0)
COLOR_UNSELECTED = (150, 150, 180)
COLOR_SELECTION_RECT = (255, 215, 0, 80)
COLOR_DISABLED = (80, 80, 100, 150)
COLOR_LOCKED = (60, 60, 80)
COLOR_BUTTON_DEFAULT = (100, 100, 100)

WINDOW_TITLE = "The Running Sloth"
SCREEN_TITLE = "The Running Sloth - Game"


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1
