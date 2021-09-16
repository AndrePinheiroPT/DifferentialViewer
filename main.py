from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_min': -1,
    'x_max': 10,
    'y_min': -1,
    'y_max': 10,
    'x_label': 'X',
    'y_label': 'Y'
}

viewer = Viewer(CONFIG)

def slide1():
    cartesian_plane()
    latex_text(r"\begin{pmatrix}2\\1\end{pmatrix}", 'vector1', (3, -2))
    linear_transformation([
        [2,viewer.mouse_state[0]], 
        [1, viewer.mouse_state[1]]
    ])
    vector(viewer.mouse_state[0], viewer.mouse_state[1], (215, 0, 0), [0, 0])
    vector(2, 1, (0, 225, 0), [0, 0])
    vector(2 + viewer.mouse_state[0], 1 + viewer.mouse_state[1], (162, 40, 255), [0, 0])

def slide2():
    cartesian_plane()
    real_functions(lambda x: x*0.5+1, -1, 10, color=(87, 0, 240))

    lim_value = limit_aproximation(lambda x: x*0.5+1, 3, 0.01)
    
    rect_sum = riemann_rectangles(lambda x: x*0.5+1, 2, 7, 30)
    latex_text(r"\displaystyle \lim_{x \to 3} f(x) = " + r"{}".format(lim_value), 'limit', (1, 3.5))
    latex_text(r"\int_{2}^{7}f(x) dx = " + r"{:.1f}".format(rect_sum), 'rect_sum', (3, 2.2))

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


viewer.set_slides([slide2, slide1, slide3, slide4])
viewer.init()

