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
    tools3D = Scense3D(1, 0, 0)
    tools3D.three_dimensional_space()
    vector(*tools3D.coord3d2d((1,0,0)), (162, 40, 255))
    #vector(*coord3d2d((0,1,0), phi, theta), (221, 70, 0))
    #vector(*coord3d2d((0,0,1), phi, theta), (0, 200, 50))
    #vector(*coord3d2d((1,1,1), phi, theta), (255, 0, 0))


viewer.set_slides([slide1])
viewer.init()

