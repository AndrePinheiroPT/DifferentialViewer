from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {'screen_width': 800, 'screen_height': 600}
viewer = Viewer(CONFIG)
grafic = GraficScene(viewer, [300, 300], 50, 50)
tools3D = Scense3D(20, 0, 0, viewer)

time = 0

def vect_field(x, y, z):
    r = 0.01 if (x**2 + y**2 + z**2) == 0 else (x**2 + y**2 + z**2)
    return [
        x/r, 
        y/r, 
        z/r]

def scene():
    #tools3D.vector((1, 1, 4), (255, 0, 0))
    #tools3D.vector_field(vect_field, [-6, 6, -6, 6,-6, 6], 5)
    tools3D.three_dimensional_space()
    
    #tools3D.parametric_surface(cone, [0, 7*tan(pi/10), 0, 2*pi], (255, 255, 255, 255))
viewer.set_slides([scene])
viewer.init()

