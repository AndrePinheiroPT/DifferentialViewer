import pygame
from pygame.locals import *
import pygame.gfxdraw
from math import *
import settings

def update_standard_values():
    global settings
    settings.standard_values = [
        (settings.CONFIG['screen_width']/2) * (settings.state[0]/settings.CONFIG['x_max'] + 1),
        (settings.CONFIG['screen_height']/2) * (1 - settings.state[1]/settings.CONFIG['y_max'])
    ]
    

def convert_coords(coords, standard):
    if standard:
        return [
            (settings.CONFIG['screen_width']/2) * (coords[0]/settings.CONFIG['x_max'] + 1),
            (settings.CONFIG['screen_height']/2) * (1 - coords[1]/settings.CONFIG['y_max'])
        ]
    else:
        return [
            (coords[0] / (settings.CONFIG['screen_width']/2) - 1) * settings.CONFIG['x_max'],
            (1 - coords[1] / (settings.CONFIG['screen_height']/2)) * settings.CONFIG['y_max']
        ]


def cartesian_plane():
    x_value = -settings.CONFIG['x_max']
    y_value = -settings.CONFIG['y_max']

    settings.screen.blit(settings.font.render(f'{settings.CONFIG["x_label"]}', False, settings.WHITE), (settings.CONFIG['screen_width'] - 30, settings.CONFIG['screen_height']/2))
    settings.screen.blit(settings.font.render(f'{settings.CONFIG["y_label"]}', False, settings.WHITE), (settings.CONFIG['screen_width']/2 + 5 , 0))
    settings.screen.blit(settings.font.render(f'0', False, settings.WHITE), (settings.CONFIG['screen_width']/2 + 5, settings.CONFIG['screen_height']/2))

    for x in range(0, settings.CONFIG['screen_width'], 100):
        pygame.draw.line(settings.screen, settings.CYAN, (x, 0), (x, settings.CONFIG['screen_height']), 1)
        if x_value != 0:
            settings.screen.blit(settings.font.render(f'{x_value:.1f}', False, settings.WHITE), (x+5, settings.CONFIG['screen_height']/2))
        x_value += settings.CONFIG['x_max'] / (ceil(settings.CONFIG['screen_width']/100) / 2)
    

    for y in range(settings.CONFIG['screen_height'], 0, -100):
        pygame.draw.line(settings.screen, settings.WHITE if y == settings.CONFIG['screen_width']/2 else settings.CYAN, (0, y), (settings.CONFIG['screen_width'], y), 1)
        if y_value != 0:
            settings.screen.blit(settings.font.render(f'{y_value:.1f}', False, settings.WHITE), (settings.CONFIG['screen_width']/2 + 5, y-22))
        y_value += settings.CONFIG['y_max'] / (ceil(settings.CONFIG['screen_height']/100) / 2)

    pygame.draw.line(settings.screen, settings.WHITE, (settings.CONFIG['screen_width']/2, 0), (settings.CONFIG['screen_width']/2, settings.CONFIG['screen_height']), 1)
    pygame.draw.line(settings.screen, settings.WHITE, (0, settings.CONFIG['screen_height']/2), (settings.CONFIG['screen_width'], settings.CONFIG['screen_height']/2), 1)


def real_functions(function, xd_min, xd_max, dx=0.01, color=(255, 255, 0)):
    
    settings.state[0] = xd_min
    function_points = []
    while xd_min <= settings.state[0] <= xd_max:
        settings.state[0] += dx

        settings.state[1] = function(settings.state[0])

        update_standard_values()
        function_points.append((settings.standard_values[0], settings.standard_values[1]))

    if len(function_points) >= 2:
        pygame.draw.lines(settings.screen, color, False, function_points, 3)


def complex_functions(func, domain_func, t_min, t_max, dt=0.01, color=(255, 255, 0)):

    complex_function_points = []
    t = t_min 
    while t_min <= t <= t_max:
        t += dt

        for i in range(0, 2):
            settings.state[i] = func(*domain_func(t))[i]

        update_standard_values()
        complex_function_points.append((settings.standard_values[0], settings.standard_values[1])) 

    if len(complex_function_points) >= 2:
        pygame.draw.lines(settings.screen, color, False, complex_function_points, 2)


def vector_field(func, space, scalar, color=(0, 255, 0)):

    for x in range(-settings.CONFIG['x_max'], settings.CONFIG['x_max']+ 1, space):
        for y in range(-settings.CONFIG['y_max'], settings.CONFIG['y_max']+ 1, space):
            vector_length = 0.001 if sqrt(func(x, y)[0]**2 + func(x, y)[1]**2) == 0 else sqrt(func(x, y)[0]**2 + func(x, y)[1]**2)

            v_stick1 = (
                0.15*(func(x, y)[1]/vector_length - func(x, y)[0]/vector_length),
                -0.15*(func(x, y)[0]/vector_length + func(x, y)[1]/vector_length)
            ) 

            v_stick2 = (
                -0.15*(func(x, y)[1]/vector_length + func(x, y)[0]/vector_length),
                0.15*(func(x, y)[0]/vector_length - func(x, y)[1]/vector_length)
            )

            output_fx = x + func(x, y)[0] * scalar
            output_fy = y + func(x, y)[1] * scalar

            pygame.draw.line(settings.screen, color, convert_coords((x, y), 1), convert_coords((output_fx, output_fy), 1), 2)
            pygame.draw.line(settings.screen, color, convert_coords((output_fx, output_fy), 1), convert_coords((output_fx + v_stick1[0], output_fy + v_stick1[1]), 1), 2)
            pygame.draw.line(settings.screen, color, convert_coords((output_fx, output_fy), 1), convert_coords((output_fx + v_stick2[0], output_fy + v_stick2[1]), 1), 2)


def derivative_line(func, x, x_min, x_max, h=0.0001, color=(230, 0, 85)):
    
    derivative = 0
    if x_min <= x <= x_max:

        derivative = (func(x+h) - func(x)) / h  # slope
        b = func(x) - derivative*x

        pygame.draw.line(settings.screen, color, 
        convert_coords((-settings.CONFIG['x_max'], -settings.CONFIG['x_max']*derivative + b), 1), 
        convert_coords((settings.CONFIG['x_max'], settings.CONFIG['x_max']*derivative + b), 1), 3)

        derivative_standards = convert_coords((x, func(x)), 1)
        for i in range(0, 2):
            derivative_standards[i] = round(derivative_standards[i])
        pygame.draw.circle(settings.screen, (255, 255, 255), derivative_standards, 4)

    return derivative


def riemann_rectangles(func, x_min, x_max, n, color_init=[131, 47, 0, 150], color_end=[231, 242, 0, 150]):
    reason_x = (convert_coords((settings.CONFIG['x_max'], settings.CONFIG['y_max']), 1)[0] - convert_coords((0, 0), 1)[0]) / settings.CONFIG['x_max']
    reason_y = (convert_coords((settings.CONFIG['x_max'], settings.CONFIG['y_max']), 1)[1] - convert_coords((0, 0), 1)[1]) / settings.CONFIG['y_max']

    color = [0, 0, 0, 0]
    d_color = [0, 0, 0, 0]
    for k in range(0, 4):
        d_color[k] = (color_end[k] - color_init[k]) / n

    dx = (x_max - x_min) / n
    total_sum = 0
    for i in range(0, n):
        for k in range(0, 4):
            color[k] = color_init[k] + d_color[k]*i

        x = x_min + i*dx
        dy = func(x)

        total_sum += dy*dx

        pygame.gfxdraw.box(settings.screen, pygame.Rect(convert_coords((x, func(x)), 1), (dx * reason_x, -dy * reason_y + 1)), color)

    return total_sum


def limit_aproximation(func, h, delta, color=(255, 255, 0)):
    real_functions(func, h - delta, h + delta)
    standard_limit = convert_coords((h, func(h)), 1)
    for i in range(0, 2):
        standard_limit[i] = round(standard_limit[i])
    pygame.draw.circle(settings.screen, color, standard_limit, 4)

    return func(h)

