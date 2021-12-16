from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {'screen_width': 800, 'screen_height': 600}
viewer = Viewer(CONFIG)
grafic = GraficScene(viewer, [300, 300], 50, 50)
tools3D = Scense3D(20, 0, 0, viewer)

time = 0

def cone(u, v):
    z = u
    y = (4 - u*tan(pi/6))*sin(v)
    return [
        (4 - u*tan(pi/6))*cos(v),
        y*cos(pi/4) - z*sin(pi/4),
        z*cos(pi/4) + y*sin(pi/4)
    ]


def scene():
    tools3D.three_dimensional_space()
    #tools3D.vector((1, 1, 2), (255, 0, 0), (1, 1, 1))
    tools3D.parametric_surface(cone, [0, 4, 0, 2*pi])
viewer.set_slides([scene])
viewer.init()

