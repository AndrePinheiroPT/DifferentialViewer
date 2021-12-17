from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {'screen_width': 800, 'screen_height': 600}
viewer = Viewer(CONFIG)
grafic = GraficScene(viewer, [300, 300], 50, 50)
tools3D = Scense3D(20, 0, 0, viewer)

time = 0


def scene():
    tools3D.three_dimensional_space()
    #tools3D.vector((1, 1, 2), (255, 0, 0), (1, 1, 1))
    #tools3D.parametric_surface(cone, [0, 7*tan(pi/10), 0, 2*pi], (255, 255, 255, 255))
viewer.set_slides([scene])
viewer.init()

