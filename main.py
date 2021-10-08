from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_min': -5,
    'x_max': 5,
    'x_length': 1,
    'y_min': -5,
    'y_max': 5,
    'y_length': 1,
    'x_label': 'X',
    'y_label': 'Y',
}

viewer = Viewer(CONFIG)
time = 0

def slide1():
    tools3D = Scense3D(8, 0, 0)
    tools3D.three_dimensional_space()

    tools3D.line([0, 0, 0], [0, 1, 0], 0, 2, (0, 0, 255), 3)
    tools3D.line([0, 2, 0], [1, 0, 0], 0, 2, (255, 0, 0), 3)
    tools3D.line([2, 2, 0], [1, 1, 3], -6, 6, (111, 111, 111))
    tools3D.vector([1, 1, 3], (0, 255, 0), (2, 2, 0))

viewer.set_slides([slide1])
viewer.init()

