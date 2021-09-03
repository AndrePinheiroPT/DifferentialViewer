from DifferentialViewerlib import math_tools
import pygame
from pygame.locals import *

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_max': 8,
    'y_max': 8,
    'x_label': 'Y',
    'y_label': 'X'
}

viewer = math_tools.Viewer(CONFIG)

def my_code():
    math_tools.cartesian_plane()

viewer.set_code(my_code)
viewer.init()

