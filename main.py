import pygame
from pygame.locals import *

# Screen configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CYAN = (50, 50, 50)

# Differential Equation state
state = [0, 0, 0]
points = []
x_max = 1
y_max = 1
coords = ('X', 'Y')

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DifferentialViewer')

draw_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

def coord_index(coord):
    if coord == 'X':
        return 0
    elif coord == 'Y':
        return 1
    elif coord == 'Z':
        return 2
    else:
        return False

standard_values = []
def update_standard_values():
    global standard_values
    # X - 0 / Y - 1 / Z - 2 
    standard_values = [
        round(state[coord_index(coords[0])] * 300/x_max) + 300,
        300 - round(state[coord_index(coords[1])] * 300/y_max)
    ]

update_standard_values()
points.append((standard_values[0], standard_values[1])) 

def cartesian_plane():
    x_value = -x_max
    y_value = y_max
    for i in range(0, 600, 100):
        pygame.draw.line(screen, CYAN, (i, 0), (i, 599), 2)
        pygame.draw.line(screen, CYAN, (0, i), (599, i), 2)

        screen.blit(font.render(f'{y_value:.1f}', False, CYAN), (312, i))
        screen.blit(font.render(f'{x_value:.1f}', False, CYAN), (i+5, 300))
        screen.blit(font.render(f'{coords[0]}', False, CYAN), (580, 300))
        screen.blit(font.render(f'{coords[1]}', False, CYAN), (280, 0))
        
        x_value += x_max / 3
        y_value -= y_max / 3


def differential(x, y, z):
    dt = 0.01
    #dx = (10 * (y - x)) * dt
    #dy = (x * (24 - z) - y) * dt
    #dz = (x * y - 8/3 * z) * dt

    dx = (-y - 0.1 * x) * dt
    dy = (x - 0.4 * y) * dt
    dz = 0

    state[0] += dx
    state[1] += dy
    state[2] += dz
    update_standard_values()
    points.append((standard_values[0], standard_values[1])) 
    pygame.draw.lines(screen, (0, 255, 0), False, points, 3)


def infinite_sum(a, b):
    global points
    for n in range(0, 10):
        if -10 < state[0] < 10 or -10 < state[1] < 10:
            prev_z0 = state[0]**2 - state[1]**2 + a
            prev_z1 = 2 * state[0] * state[1] + b 
            state[0] = prev_z0
            state[1] = prev_z1
            update_standard_values()
            points.append((standard_values[0], standard_values[1])) 

    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 2)
    

clock = pygame.time.Clock()
while True:
    clock.tick(100)
    screen.fill((0, 0, 0))
    mouse_state = [
        (pygame.mouse.get_pos()[0] / 300 - 1) * x_max,
        (1 - pygame.mouse.get_pos()[1] / 300) * y_max
    ]
    cartesian_plane()

    #differential(state[0], state[1], state[2])
    infinite_sum(mouse_state[0], mouse_state[1])
    
    pygame.draw.circle(screen, (255, 255, 255), (standard_values[0], standard_values[1]), 3)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            state = [0, 0, 0]
            update_standard_values()
            points = [(standard_values[0], standard_values[1])]
    
    pygame.display.update()

