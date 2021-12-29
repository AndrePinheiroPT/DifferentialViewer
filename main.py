from Matiklib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {'screen_width': 800, 'screen_height': 600}
viewer = Viewer(CONFIG)
grafic1 = Graph(viewer, [0, 0], 400, 600, 50, 50, 'Re', 'Im')
grafic2 = Graph(viewer, [400, 0], 400, 600, 25, 25, 'Re', 'Im')
tools3D = Scense3D(10, 0, 0, viewer)

time = 0

def vect_field(x, y, z):
    r = 0.01 if (x**2 + y**2 + z**2) == 0 else (x**2 + y**2 + z**2)
    return [-x/r, -y/r, -z/r]

def scene():
    global time
    tools3D.phi = time
    
    tools3D.cartesian_plane3D()
    tools3D.vector((1, 0, 0), (255, 0, 0))
    tools3D.vector((-2, -2, 3), (255, 0, 0))
    tools3D.vector_field(vect_field, [-6, 6, -6, 6,-6, 6], 4)
    time += 0.01


points_list = [
    [0, 0],   # z1 = a + bi
]
quadratic_point = [1, 0]
def quadratic_domain(t):
    return [1, ]



def minigrath_test():
    global euler_identity
    grafic1.cartesian_plane()
    grafic2.cartesian_plane()

    grafic1.parametric_functions(lambda t: [1, t], -10, 10)
    grafic1.manipulation_points(points_list, [10, 10, 10, 10])
    grafic1.dot(points_list[0])

    euler_identity = [points_list[0][0]**2 - points_list[0][1]**2, 2*points_list[0][0]*points_list[0][1]]
    grafic2.dot(euler_identity)
    grafic2.vector(euler_identity, (255, 255, 0))
    grafic2.complex_functions(lambda a, b: [a**2 - b**2, 2*a*b], lambda t: [1, t], -10, 10)

viewer.set_slides([minigrath_test])
viewer.init()

