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


tools3D = Scense3D(13, 2, 1, viewer)
def slide1():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)
    tools3D.parametric_line(helicoide, -10, -0.2*(viewer.time-10)**2 + 10.1 if viewer.time < 10 else 10, (0, 0, 255))
    #tools3D.parametric_surface(sphere, [-pi, pi, -pi, pi])

def slide2():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)
    if viewer.time < 10:
        tools3D.parametric_line(helicoide, -10, -0.2*(viewer.time)**2 + 10.1 if viewer.time < 10 else -10, (0, 0, 255))

def func(t):
    return [t, 0, 0.21*t**3 - 1.22*t**2 - 0.4*t + 8]
def slide3():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)
    tools3D.parametric_line(func, 0, 5)

def func_surface(u, v):
    return [u, sin(v)*(0.21*u**3 - 1.22*u**2 - 0.4*u + 8), (0.21*u**3 - 1.22*u**2 - 0.4*u + 8)*cos(v)]
def slide4():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)
    tools3D.parametric_line(func, 0, 5)
    tools3D.parametric_surface(func_surface, [0, 5, 0, -0.5/pi*(viewer.time - 2*pi)**2 + 2*pi if viewer.time < 2*pi else 2*pi], dv=0.3, du=0.3)
def slide5():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)
    tools3D.parametric_surface(func_surface, [0, 5, 0, -0.5/pi*(viewer.time)**2 + 2*pi if viewer.time < 2*pi else 0], dv=0.3, du=0.3)


def cossin(x, y):
    return sin(x)*cos(y) + 4

def cossin_gradient(x, y, z): 
    return [cos(x), -sin(y), 0]

def slide6():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)  
    tools3D.function(cossin, [-10, -0.2*(viewer.time-10)**2 + 10.1 if viewer.time < 10 else 10, -10, 10])
    viewer.time += 0.6

def slide7():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)  
    tools3D.function(cossin, [-10, 10, -10, 10])
    tools3D.vector_field(cossin_gradient, [-10, -0.2*(viewer.time-10)**2 + 10.1 if viewer.time < 10 else 10, -10, 10, 0, 0], 1)
    viewer.time += 0.6

def slide8():
    tools3D.phi += 0.006
    tools3D.three_dimensional_space(10)  
    if viewer.time < 10:
        tools3D.function(cossin, [-10, -0.2*(viewer.time)**2 + 10.1 if viewer.time < 10 else -10, -10, 10])
        tools3D.vector_field(cossin_gradient, [-10,  -0.2*(viewer.time)**2 + 10.1 if viewer.time < 10 else -10, -10, 10, 0, 0], 1)
    viewer.time += 0.6

time=0
def slide9():
    global time
    tools3D.phi += 0.006
    tools3D.r=30
    tools3D.three_dimensional_space(10)  
    tools3D.differential(lorenz_attractor, [1, 1.4, 4], time)
    time+=0.01

grafic = GraficScene([40, 40], 80, 80, viewer)
def test():
    grafic.check_mouse()
    grafic.cartesian_plane()
    grafic.real_functions(lambda x: -x**2, -4, 4)

viewer.set_slides([test])
viewer.init()

