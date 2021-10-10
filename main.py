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

def helicoide(l):
    return [cos(l), sin(l), l]

def sphere(u, v):
    return [5 + 2*cos(u)*sin(v), 2*sin(u)*sin(v), 2*cos(v)]

def vector_f(x, y, z):
    return [
        x / (0.01 if (x**2 + y**2 + z**2) == 0 else (x**2 + y**2 + z**2)),
        y / (0.01 if (x**2 + y**2 + z**2) == 0 else (x**2 + y**2 + z**2)),
        z / (0.01 if (x**2 + y**2 + z**2) == 0 else (x**2 + y**2 + z**2))
    ]

tools3D = Scense3D(13, 2, 2)
def slide1():
    global time, tools3D
    
    tools3D.three_dimensional_space(10)
    tools3D.vector_field(vector_f, [-6, 6, -6, 6, -6, 6], 3, branch_length=0.03)
    tools3D.parametric_line(helicoide, -10, 10, (0, 0, 255))
    tools3D.parametric_surface(sphere, [-pi, pi, -pi, pi])
    tools3D.differential(lorenz_attractor, [1, 1.4, 4], time)
    time += 0.01


viewer.set_slides([slide1])
viewer.init()

