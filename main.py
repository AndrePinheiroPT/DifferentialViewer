import pygame
from pygame.locals import *

# Screen configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Differential Equation state
state = [5, 2, 1]
points = []
x_max = 20
y_max = 45

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DifferentialViewer')

draw_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Times', 20)

standard_values = []
def update_standard_values():
    standard_values = [
        round(state[0] * 300/x_max) + 300,
        300 - round(state[2] * 300/y_max)
    ]

update_standard_values()
points.append((standard_values[0], standard_values[1])) 

def cartesian_plane():
    x_value = -x_max
    y_value = y_max
    for i in range(0, 600, 100):
        pygame.draw.line(screen, (25, 25, 25), (i, 0), (i, 599), 2)
        pygame.draw.line(screen, (25, 25, 25), (0, i), (599, i), 2)

        text_y = font.render(f'{y_value:.1f}', False, (55, 55, 55))
        text_x = font.render(f'{x_value:.1f}', False, (55, 55, 55))
        screen.blit(text_y, (305, i))
        screen.blit(text_x, (i+5, 300))
        x_value += x_max / 3
        y_value -= y_max / 3


def differential(x, y, z):
    dt = 0.01
    dx = (10 * (y - x)) * dt
    dy = (x * (24 - z) - y) * dt
    dz = (x * y - 8/3 * z) * dt
    state[0] += dx
    state[1] += dy
    state[2] += dz
    update_standard_values()

clock = pygame.time.Clock()
while True:
    clock.tick(100)
    screen.fill((0, 0, 0))

    cartesian_plane()
    differential(state[0], state[1], state[2])

    pygame.draw.circle(screen, (255, 255, 255), (standard_values[0], standard_values[1]), 3)

    points.append((standard_values[0], standard_values[1])) 
    pygame.draw.lines(screen, (0, 255, 0), False, points)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    
    pygame.display.update()

