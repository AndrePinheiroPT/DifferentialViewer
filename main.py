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

def gauss_curve(x, y):
    return 4*exp(-(x**2 + y**2))

def lorenz_attractor(coords):
    dx = (10 * (coords[1] - coords[0]))
    dy = (coords[0] * (24 - coords[2]) - coords[1])
    dz = (coords[0] * coords[1] - 8/3 * coords[2])
    return [dx, dy, dz]

def slide1():
    global time
    tools3D = Scense3D(30, 2, 2)
    tools3D.three_dimensional_space(10)

    tools3D.line([0, 0, 0], [0, 1, 0], 0, 2, (0, 0, 255), 3)
    tools3D.line([0, 2, 0], [1, 0, 0], 0, 2, (255, 0, 0), 3)
    tools3D.line([2, 2, 0], [1, 1, 3], -6, 6, (111, 111, 111))
    tools3D.vector([1, 1, 3], (0, 255, 0), (2, 2, 0))
    tools3D.function(gauss_curve, [-6, 6, -6, 6])
    tools3D.differential(lorenz_attractor, [1, 1.4, 4], time)
    time += 0.01


viewer.set_slides([slide1])
viewer.init()

