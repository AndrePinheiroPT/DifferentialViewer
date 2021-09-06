from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_max': 5.8,
    'y_max': 10.1,
    'x_min': -1.4,
    'y_min': -10.2,
    'x_label': 'X',
    'y_label': 'Y'
}

viewer = Viewer(CONFIG)

def slide1():
    
    cartesian_plane()
    linear_transformation([[1.5,-1], [-1, 2]])
    real_functions(lambda x: (x-3)*(x+2)*(x+1)+4, -6, 6, color=(87, 0, 240))

def slide2():
    cartesian_plane()
    real_functions(lambda x: (x-3)*(x+2)*(x+1)+4, -6, 6, color=(87, 0, 240))
    derivative_line(lambda x: (x-3)*(x+2)*(x+1)+4, viewer.mouse_state[0], 3)

def slide3():
    cartesian_plane()
    real_functions(lambda x: (x-3)*(x+2)*(x+1)+4, -6, 6, color=(87, 0, 240))
    limit_aproximation(lambda x: (x-3)*(x+2)*(x+1)+4, 3, 0.5)
    derivative_line(lambda x: (x-3)*(x+2)*(x+1)+4, viewer.mouse_state[0], 3)

def slide4():
    cartesian_plane()
    riemann_rectangles(lambda x: (x-3)*(x+2)*(x+1)+4, 0, 2.75, 10)
    real_functions(lambda x: (x-3)*(x+2)*(x+1)+4, -6, 6, color=(87, 0, 240))
    limit_aproximation(lambda x: (x-3)*(x+2)*(x+1)+4, 3, 0.5)
    derivative_line(lambda x: (x-3)*(x+2)*(x+1)+4, viewer.mouse_state[0], 3)


viewer.set_slides([slide1, slide2, slide3, slide4])
viewer.init()

