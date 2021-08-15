import pygame
import graph_tools

CONFIG = {
    'screen_width': 600,
    'screen_height': 600,
    'x_max': 8,
    'y_max': 8,
    'x_label': 'Re',
    'y_label': 'Im'
}

CYAN = (55, 55, 55)
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((CONFIG['screen_width'], CONFIG['screen_height']))
pygame.display.set_caption('DifferentialViewer')

draw_surface = pygame.Surface((CONFIG['screen_width'], CONFIG['screen_height']))

pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

state = [0, 0]
standard_values = []
time = 0
