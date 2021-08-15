from graph_tools import *
from math import *
import settings

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


def zeta_function(a, b):
    r_output = 0
    i_output = 0
    for n in range(1, 501):
        r_f = (-2**(1-a) * cos(b*log(2)) + 1) / ((-2**(1-a) * cos(b*log(2)) + 1)**2 + (2**(1-a) * sin(b*log(2)))**2) 
        i_f = (-2**(1-a) * sin(b*log(2))) / ((-2**(1-a) * cos(b*log(2)) + 1)**2 + (2**(1-a) * sin(b*log(2)))**2)

        r_g = (-1)**(n-1) * (cos(b*log(n)) / (n**a))
        i_g = (-1)**(n-1) * (-sin(b * log(n)) / (n**a))

        r_output += r_f * r_g - i_f * i_g
        i_output += r_f * i_g + i_f * r_g

    return [r_output, i_output]


def zeta_domain(t):
    return [0.5, t]


def vector_f(x, y):
    f_x = y**3 - 9*y
    f_y = x**3 - 9*x
    return [f_x, f_y]


clock = pygame.time.Clock()
while True:
    clock.tick(100)
    settings.screen.fill((0, 0, 0))
    mouse_state = [
        (pygame.mouse.get_pos()[0] / (settings.CONFIG['screen_width']/2) - 1) * settings.CONFIG['x_max'],
        (1 - pygame.mouse.get_pos()[1] / (settings.CONFIG['screen_height']/2)) * settings.CONFIG['y_max']
    ]

    cartesian_plane()
    #real_functions(lambda x: sin(x), -6, 6)
    vector_field(vector_f, 1)
    #if len(points) >= 2:
        #pygame.draw.lines(screen, (0, 255, 0), False, points, 1)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    settings.time += 0.01
    pygame.display.update()