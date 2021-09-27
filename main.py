from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_min': -10,
    'x_max': 10,
    'x_length': 5,
    'y_min': -10,
    'y_max': 10,
    'y_length': 5,
    'x_label': 'X',
    'y_label': 'Y'
}

viewer = Viewer(CONFIG)
time = 0

def slide1():
    cartesian_plane()
    #latex_text(r"\begin{pmatrix}2\\1\end{pmatrix}", 'vector1', (3, -2))
    linear_transformation([
        [2,viewer.mouse_state[0]], 
        [1, viewer.mouse_state[1]]
    ])
    vector(viewer.mouse_state[0], viewer.mouse_state[1], (215, 0, 0))
    vector(2, 1, (0, 225, 0))
    vector(2 + viewer.mouse_state[0], 1 + viewer.mouse_state[1], (162, 40, 255))

def slide2():
    cartesian_plane()
    real_functions(lambda x: x*0.5+1, -1, 10, color=(87, 0, 240))

    lim_value = limit_aproximation(lambda x: x*0.5+1, 3, 0.01)
    
    rect_sum = riemann_rectangles(lambda x: x*0.5+1, 2, 7, 30)
    #latex_text(r"\displaystyle \lim_{x \to 3} f(x) = " + r"{}".format(lim_value), 'limit', (1, 3.5))
    #latex_text(r"\int_{2}^{7}f(x) dx = " + r"{:.1f}".format(rect_sum), 'rect_sum', (3, 2.2))

def lorenz(init_c):
    dx = (10*(init_c[2] - init_c[0]))*0.01
    dy = (init_c[0]*(28 - init_c[1]) - init_c[2])*0.01
    dz = (init_c[0]*init_c[2] - 8/3*init_c[1])*0.01
    return [dx, dz, dy]

def slide3():
    global time
    cartesian_plane()
    differential(lorenz, [-6, 30, 0], time, color=(255, 255, 0), dt=0.01)
    time += 0.01

def circle(t):
    x = 5*cos(t)
    y = 5*sin(t)
    return [x, y]

theta = 0
def slide4():
    global theta
    cartesian_plane()
    parametric_functions(circle, 0, 2*pi, color=(0, 200, 0))
    vector(5*cos(theta), 5*sin(theta), (255, 225, 0))
    #latex_text(r"e^{i" + rf"{theta:.2f}" + r"}", f'euler_i{theta:.2f}', [5*cos(theta) ,5*sin(theta)])
    theta += 0.01


viewer.set_slides([slide2, slide1, slide3, slide4])
viewer.init()

