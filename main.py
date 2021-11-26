from DifferentialViewerlib.math_tools import *
import pygame
from pygame.locals import *

CONFIG = {'screen_width': 800, 'screen_height': 600}
viewer = Viewer(CONFIG)
grafic = GraficScene(viewer, [300, 300], 70, 70)

time = 0
alpha = [0.01, 0]
points_list = []
points_list.append(alpha)

def trignometric_circle(t):
    return [cos(t), sin(t)]

def arc(t):
    return [0.25*cos(t), 0.25*sin(t)]

def sin_slide():
    global points_list
    grafic.cartesian_plane()
    grafic.parametric_functions(trignometric_circle, 0, 2*pi, (230, 230, 230))
    grafic.parametric_functions(arc, 0, points_list[0][0], (255, 255, 0))
    
    grafic.line([0, 0], points_list[0], stroke=3)
    grafic.line([0, 0], [cos(points_list[0][0]), sin(points_list[0][0])], (255, 255, 255), 4)
    grafic.line([points_list[0][0], 0], [points_list[0][0], sin(points_list[0][0])], (255, 0, 0), 4)
    
    grafic.circle(points_list[0], 6)

    grafic.line([cos(points_list[0][0]), sin(points_list[0][0])], [points_list[0][0], sin(points_list[0][0])], (255, 0, 0), 3)
    grafic.real_functions(lambda x: sin(x), 0, points_list[0][0], color=(255,0, 0))
    points_list = grafic.manipulation_points(points_list, [6, 6, 6, 6])
    points_list[0][1] = 0

    grafic.vector([2,1], (255, 255, 255))


viewer.set_slides([sin_slide])
viewer.init()

