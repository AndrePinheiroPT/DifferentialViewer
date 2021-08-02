import pygame
from pygame.locals import *
from math import *

# Screen configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CYAN = (50, 50, 50)

# Differential Equation state
state = [0, 0, 0]
points = []
function_points = []
x_max = 4
y_max = 2
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
        (SCREEN_WIDTH/2) * (state[coord_index(coords[0])]/x_max + 1),
        (SCREEN_HEIGHT/2) * (1 - state[coord_index(coords[1])]/y_max)
    ]

update_standard_values()
points.append((standard_values[0], standard_values[1])) 

def cartesian_plane():
    x_value = -x_max
    y_value = -y_max
    for x in range(0, SCREEN_WIDTH, 100):
        pygame.draw.line(screen, CYAN, (x, 0), (x, SCREEN_HEIGHT), 2)
        screen.blit(font.render(f'{x_value:.1f}', False, CYAN), (x+5, SCREEN_HEIGHT/2))
        x_value += x_max / (ceil(SCREEN_WIDTH/100) / 2)
        
    for y in range(SCREEN_HEIGHT, 0, -100):
        pygame.draw.line(screen, CYAN, (0, y), (SCREEN_WIDTH, y), 2)
        screen.blit(font.render(f'{y_value:.1f}', False, CYAN), (SCREEN_WIDTH/2 + 10, y))
        y_value += y_max / (ceil(SCREEN_HEIGHT/100) / 2)


def real_functions(xd_min, xd_max, dx, sum_length=1):
    global function_points, state

    state[0] = xd_min
    function_points = []
    while xd_min <= state[0] <= xd_max:
        state[0] += dx
        for n in range(1, sum_length+1): 
            state[1] = 0
            # PUT THE CODE OF THE FUNCTION HERE

            state[1] += 1/state[0]

            # PUT THE CODE OF THE FUNCTION HERE
        update_standard_values()
        function_points.append((standard_values[0], standard_values[1]))


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


def complex_conjectures(a, b, sum_length):
    global points
    for n in range(1, sum_length+1):
        if -(x_max + 1000) < state[0] < x_max + 1000 and -(y_max + 1000) < state[1] < y_max + 1000:
            prev_z0 = state[0]**2 - state[1]**2 + a
            prev_z1 = 2 * state[0] * state[1] + b 
            
            state[0] += prev_z0
            state[1] += prev_z1
            
            update_standard_values()
            points.append((standard_values[0], standard_values[1]))

    pygame.draw.circle(screen, (255, 255, 255), (standard_values[0], standard_values[1]), 3)
    
    state = [0, 0, 0]
    update_standard_values()
    points = [(standard_values[0], standard_values[1])]


def complex_functions(a, b, sum_lenght, draw=True):
    global points, function_points

    # PUT THE CODE OF THE FUNCTION HERE
    for n in range(1, sum_lenght+1):
        r_f = (-2**(1-a) * cos(b*log(2)) + 1) / ((-2**(1-a) * cos(b*log(2)) + 1)**2 + (2**(1-a) * sin(b*log(2)))**2) 
        i_f = (-2**(1-a) * sin(b*log(2))) / ((-2**(1-a) * cos(b*log(2)) + 1)**2 + (2**(1-a) * sin(b*log(2)))**2)

        r_g = (-1)**(n-1) * (cos(b*log(n)) / (n**a))
        i_g = (-1)**(n-1) * (-sin(b * log(n)) / (n**a))

        r_output = r_f * r_g - i_f * i_g
        i_output = r_f * i_g + i_f * r_g

        state[0] += r_output
        state[1] += i_output

        update_standard_values()
        points.append((standard_values[0], standard_values[1])) 

    # PUT THE CODE OF THE FUNCTION HERE

    if draw:
        function_points.append((standard_values[0], standard_values[1]))

    pygame.draw.circle(screen, (255, 255, 255), (standard_values[0], standard_values[1]), 3)
    
    state = [0, 0, 0]
    update_standard_values()
    points = [(standard_values[0], standard_values[1])]


clock = pygame.time.Clock()
while True:
    clock.tick(100)
    screen.fill((0, 0, 0))
    mouse_state = [
        (pygame.mouse.get_pos()[0] / (SCREEN_WIDTH/2) - 1) * x_max,
        (1 - pygame.mouse.get_pos()[1] / (SCREEN_HEIGHT/2)) * y_max
    ]
    
    cartesian_plane()

    #differential(state[0], state[1], state[2])
    #complex_conjectures(mouse_state[0], mouse_state[1], 1000)
    #complex_functions(0.5, k, 50000)
    real_functions(-4, 0, 0.01)
    

    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 1)
    if len(function_points) >= 2:
        pygame.draw.lines(screen, (255, 255, 0), False, function_points, 2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    pygame.display.update()

