from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_min': -6,
    'x_max': 6,
    'y_min': -6,
    'y_max': 6,
    'x_label': 'X',
    'y_label': 'Y'
}

viewer = Viewer(CONFIG)

def slide1():
    cartesian_plane()
    latex_text('x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}', 'quadratic', (0, 0), 0.1)
    linear_transformation([
        [3,2], 
        [-2, 1]
    ])
    vector(2, 1, (215, 0, 0), [0, 0])
    vector(3, -2, (0, 225, 0), [0, 0])
    vector(5, -1, (162, 40, 255), [0, 0])

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

