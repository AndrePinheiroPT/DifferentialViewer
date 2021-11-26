import pygame
import pygame.gfxdraw
from sympy import preview
import os
import numpy as np
from PIL import Image
from pygame.locals import *
from math import *
from io import BytesIO 
import shutil 

CONFIG = {
    'screen_width': 900,
    'screen_height': 600
}

CYAN = (55, 55, 55)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
standard_values = []
screen = None
font = None

class Viewer():
    def __init__(self, config):
        self.mouse_pressed = False
        self.slide_index = 0
        self.slides = []
        self.mouse_state = []
        self.config = config
        self.time = 0

        path = os.path.dirname(os.path.realpath(__file__)) + '/img'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    
    def set_slides(self, slides):
        self.slides = slides

    def set_config(self, config):
        self.config = config

    def init(self):
        global screen, font, CONFIG
        CONFIG = self.config
        pygame.init()

        screen = pygame.display.set_mode((CONFIG['screen_width'], CONFIG['screen_height']))
        pygame.display.set_caption('DifferentialViewer')
        pygame.Surface((CONFIG['screen_width'], CONFIG['screen_height']))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 15)
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(100)
            screen.fill((0, 0, 0))
            self.mouse_state = pygame.mouse.get_pos()
            
            self.slides[self.slide_index]()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.slide_index >= 1:
                            self.slide_index -= 1
                            self.time = 0
                    if event.key == pygame.K_RIGHT:
                        if self.slide_index < len(self.slides) - 1:
                            self.slide_index += 1
                            self.time = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pressed = False

            self.time += 0.1
            pygame.display.update()

class GraficScene:
    def __init__(self, viewer, origin_coords, unit_x, unit_y, x_label='X', y_label='Y'):
        self.origin_coords = origin_coords
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.x_label = x_label
        self.y_label = y_label
        self.prev_state = None
        self.object_selected = None
        self.viewer = viewer

    def check_mouse(self):
        mouse_state = self.convert_coords(pygame.mouse.get_pos(), 0)
        
        if self.viewer.mouse_pressed:
            if self.prev_state == None:
                self.prev_state = mouse_state
            self.origin_coords[0] += -(self.prev_state[0] - mouse_state[0])*60
            self.origin_coords[1] += (self.prev_state[1] - mouse_state[1])*60
            self.prev_state = mouse_state
        else:
            self.prev_state = None

    def manipulation_points(self, points_list, hitbox):
        points = points_list
        if self.object_selected == None:
            for key, point in enumerate(points):
                if (self.convert_coords(point, 1)[0] - hitbox[0] <= self.viewer.mouse_state[0] <= self.convert_coords(point, 1)[0] + hitbox[2]) and (self.convert_coords(point, 1)[1] - hitbox[1] <= self.viewer.mouse_state[1] <= self.convert_coords(point, 1)[1] + hitbox[3]) and self.viewer.mouse_pressed:
                    self.object_selected = key
                     
                    points[key] = self.convert_coords(self.viewer.mouse_state, 0)
                    break
        elif self.viewer.mouse_pressed:
            points_list[self.object_selected] = self.convert_coords(self.viewer.mouse_state, 0)
        else:
            self.object_selected = None
        return points_list

    def convert_coords(self, coords, standard):
        if standard:
            return [coords[0]*self.unit_x + self.origin_coords[0], -coords[1]*self.unit_x + self.origin_coords[1]]
        else:
            return [(coords[0] - self.origin_coords[0])/self.unit_y,-(coords[1] - self.origin_coords[1])/self.unit_y]

    def cartesian_plane(self, move_grid=True):
        if move_grid and self.object_selected == None:
            self.check_mouse()

        x = self.origin_coords[0]
        x_value = 0
        while x <= CONFIG['screen_width']:
            pygame.draw.line(screen, CYAN, (x, 0), (x, CONFIG['screen_height']), 1)
            screen.blit(font.render(f'{x_value:.1f}', False, WHITE), (x + 2 , self.origin_coords[1]))
            x += self.unit_x
            x_value += 1
            
        x = self.origin_coords[0]
        x_value = 0
        while x >= 0:
            pygame.draw.line(screen, CYAN, (x, 0), (x, CONFIG['screen_height']), 1)
            screen.blit(font.render(f'{x_value:.1f}', False, WHITE), (x + 2 , self.origin_coords[1]))
            x -= self.unit_x
            x_value -= 1

        y = self.origin_coords[1]
        y_value = 0
        while y <= CONFIG['screen_height']:
            pygame.draw.line(screen, CYAN, (0, y), (CONFIG['screen_width'], y), 1)
            if y_value != 0:
                screen.blit(font.render(f'{y_value:.1f}', False, WHITE), (self.origin_coords[0]+2, y-14))
            y += self.unit_y
            y_value -= 1

        y = self.origin_coords[1]
        y_value = 0
        while y >= 0:
            pygame.draw.line(screen, CYAN, (0, y), (CONFIG['screen_width'], y), 1)
            if y_value != 0:
                screen.blit(font.render(f'{y_value:.1f}', False, WHITE), (self.origin_coords[0]+2, y-14))
            y -= self.unit_y
            y_value += 1
        
        screen.blit(font.render(f'{self.x_label}', False, WHITE), (CONFIG['screen_width']-10, self.origin_coords[1]-14))
        screen.blit(font.render(f'{self.y_label}', False, WHITE), (self.origin_coords[0]-12, 0))
        pygame.draw.line(screen, WHITE, (self.origin_coords[0], 0), (self.origin_coords[0], CONFIG['screen_height']), 1)
        pygame.draw.line(screen, WHITE, (0, self.origin_coords[1]), (CONFIG['screen_width'], self.origin_coords[1]), 1)

    def linear_transformation(self, matrix):
        alpha = CONFIG['screen_width']/(0.001 if matrix[0][0] == 0 else matrix[0][0])
        beta = CONFIG['screen_height']/(0.001 if matrix[1][1] == 0 else matrix[1][1])

        n = -10
        while n <= 10:
            pygame.draw.line(screen, YELLOW, 
            self.convert_coords((-beta*matrix[0][1] + n*matrix[0][0], -beta*matrix[1][1] + n*matrix[1][0]), 1), 
            self.convert_coords((beta*matrix[0][1] + n*matrix[0][0], beta*matrix[1][1] + n*matrix[1][0]), 1))
            n += 1

        n = -10
        while n <= 10:
            pygame.draw.line(screen, YELLOW, 
            self.convert_coords((-alpha*matrix[0][0] + n*matrix[0][1], -alpha*matrix[1][0] + n*matrix[1][1]), 1), 
            self.convert_coords((alpha*matrix[0][0] + n*matrix[0][1], alpha*matrix[1][0] + n*matrix[1][1]), 1))
            n += 1
    
    def real_functions(self, function, xd_min, xd_max, dx=0.01, color=(255, 255, 0)):
        x = xd_min if xd_min <= xd_max else xd_max
        function_points = []

        function_points.append(self.convert_coords((x, function(x)), 1))
        while x <= (xd_max if xd_min < xd_max else xd_min):
            x += dx
            y = function(x)

            function_points.append(self.convert_coords((x, y), 1))

        if len(function_points) >= 2:
            pygame.draw.lines(screen, color, False, function_points, 3)

    def complex_functions(self, func, domain_func, t_min, t_max, dt=0.01, color=(255, 255, 0)):
        complex_function_points = []
        t = t_min if t_min <= t_max else t_max

        
        while t <= (t_max if t_min < t_max else t_min):
            t += dt
            z = []
            for i in range(0, 2):
                z.append(func(*domain_func(t))[i])

            complex_function_points.append(self.convert_coords((z[0], z[1]), 1))

        if len(complex_function_points) >= 2:
            pygame.draw.lines(screen, color, False, complex_function_points, 2)
    
    def derivative_line(self, func, x, range_line, h=0.0001, color=(230, 0, 85)):
        derivative = 0

        derivative = (func(x+h) - func(x)) / h  # slope
        b = func(x) - derivative*x

        x_range = range_line/(1+derivative**2)**0.5
        pygame.draw.line(screen, color, 
        self.convert_coords((x - x_range, (x - x_range)*derivative + b), 1), 
        self.convert_coords((x + x_range, (x + x_range)*derivative + b), 1), 3)
            
        return derivative

    def riemann_rectangles(self, func, x_min, x_max, n, color_init=[131, 47, 0, 200], color_end=[231, 242, 0, 200]):
        reason_x = (self.convert_coords((CONFIG['x_max'], CONFIG['y_max']), 1)[0] - self.convert_coords((0, 0), 1)[0]) / CONFIG['x_max']
        reason_y = (self.convert_coords((CONFIG['x_max'], CONFIG['y_max']), 1)[1] - self.convert_coords((0, 0), 1)[1]) / CONFIG['y_max']

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

            pygame.gfxdraw.box(screen, pygame.Rect(self.convert_coords((x, func(x)), 1), (dx * reason_x, -dy * reason_y + 1)), color)

        return total_sum

    def limit_aproximation(self, func, h, delta, r=True, color=(255, 255, 0)):
        self.real_functions(func, h - delta, h + delta)
        standard_limit = self.convert_coords((h, func(h)), 1)
        for i in range(0, 2):
            standard_limit[i] = round(standard_limit[i])
        pygame.draw.circle(screen, color, standard_limit, 4)

        return func(h + delta if r else h - delta)

    def latex_text(self, formula, name_file, position=None, dpi=150):
        obj = BytesIO()
        preview(rf'$${formula}$$', filename='{}.png'.format(name_file), euler=False, outputbuffer=obj, viewer='BytesIO', dvioptions=["-T", "tight", "-z", "0", "--truecolor", f"-D {dpi}", "-bg", "Transparent", "-fg", "White"])
        obj.seek(0)
        formula = pygame.image.load(obj)
        screen.blit(formula, self.convert_coords(position, 1))

    def parametric_functions(self, func, t_min, t_max, color=(255, 255, 0), dt=0.01):
        point_list = []
        t = t_min if t_min <= t_max else t_max

        point_list.append(self.convert_coords(func(t), 1))
        while t <= (t_max if t_min < t_max else t_min):
            point_list.append(self.convert_coords(func(t), 1))
            t += dt
        
        pygame.draw.lines(screen, color, False, point_list, 3)

    def bazier_curve(self, points_list, t_max, color=(255, 255, 0), dt=0.01):
        bezier_points = []
        t = 0
        while t < t_max:
            points = points_list
            while len(points) > 1:
                new_points_list = []
                for i in range(0, len(points) - 1):
                    new_points_list.append([
                        points[i][0] + t*(points[i + 1][0] - points[i][0]), 
                        points[i][1] + t*(points[i + 1][1] - points[i][1])
                    ])
                points = new_points_list
            
            bezier_points.append(self.convert_coords(points[0], 1))
            t += dt
        
        pygame.draw.lines(screen, color, False, bezier_points, 3)
        
    def line(self, init_point, end_point, color=(255, 255, 0), stroke=1):
        pygame.draw.line(screen, color, self.convert_coords(init_point, 1), self.convert_coords(end_point, 1), stroke)

    def circle(self, coords, radius, color=(255, 255, 0)):
        integer_coords = [round(self.convert_coords(coords, 1)[0]), round(self.convert_coords(coords, 1)[1])]
        pygame.draw.circle(screen, color, integer_coords, radius)

    def vector(self, vect, color, origin=[0, 0], stroke=4, branch_length=0.2):
        dx = vect[0]
        dy = vect[1]

        vector_length = 0.001 if sqrt(dx**2 + dy**2) == 0 else sqrt(dx**2 + dy**2)

        branch1 = (branch_length*(dy/vector_length - dx/vector_length), -branch_length*(dx/vector_length + dy/vector_length)) 
        branch2 = (-branch_length*(dy/vector_length + dx/vector_length), branch_length*(dx/vector_length - dy/vector_length))

        x_component = origin[0] + dx
        y_component = origin[1] + dy
        triangle = [self.convert_coords((x_component, y_component), 1), self.convert_coords((x_component + branch1[0], y_component + branch1[1]), 1), self.convert_coords((x_component + branch2[0], y_component + branch2[1]), 1)]
        pygame.draw.line(screen, color, self.convert_coords((origin[0], origin[1]), 1), self.convert_coords((x_component, y_component), 1), stroke)
        pygame.gfxdraw.filled_polygon(screen, triangle, color)

    def vector_field(self, vect_func, xyz_limits, dist, color=(0, 255, 0), branch_length=0.01):
        x = xyz_limits[0]
        while x <= xyz_limits[1]:
            y = xyz_limits[2]
            while y <= xyz_limits[3]:
                z = xyz_limits[4]
                while z <= xyz_limits[5]:
                    self.vector(vect_func(x, y, z), color, (x, y, z), 2, branch_length=branch_length)
                    z += dist
                y += dist
            x += dist


class Scense3D:
    def __init__(self, r, theta, phi, viewer):
        self.r = r
        self.theta = theta
        self.phi = phi 
        self.can_change = False
        self.prev_state = None
        self.viewer = viewer
        self.dxy = [0, 0]

    def coord3d2d(self, point):
        self.check_mouse()
        matrix = (
            ((1/self.r)*cos(self.phi), -(1/self.r)*sin(self.phi), 0),
            ((1/self.r)*sin(self.phi)*cos(self.theta), (1/self.r)*cos(self.phi)*cos(self.theta), (1/self.r)*sin(self.theta)),
            (0, 0, 0)
        )

        new_point = [0, 0]
        for k in range(0, 2):
            for i in range(0, 3):
                new_point[k] += matrix[k][i]*point[i]
                
        return new_point

    def convert(self, coords, standard=True):
        if standard:
            return [
                CONFIG['screen_width']/2*(coords[0] + 1),
                CONFIG['screen_height']/2*(1 - coords[1])
            ]
        else:
            return [
                coords[0]*2 / CONFIG['screen_width'] - 1,
                -coords[1]*2 / CONFIG['screen_height'] + 1
            ]

    def check_mouse(self):
        mouse_state = self.convert(pygame.mouse.get_pos(), 0)
        if self.viewer.mouse_pressed:
            if not self.can_change:
                self.prev_state = mouse_state
            self.theta = self.dxy[0] + mouse_state[1] - self.prev_state[1]
            self.phi = self.dxy[1] + mouse_state[0] - self.prev_state[0]
            self.can_change = True
        else:
            if self.can_change:
                self.dxy = [self.theta, self.phi]
            self.can_change = False
            
    def vector(self, vect, color, origin=[0, 0, 0], stroke=3, branch_length=0.03):
        dx = self.coord3d2d(vect)[0]
        dy = self.coord3d2d(vect)[1]

        vector_length = 0.001 if sqrt(dx**2 + dy**2) == 0 else sqrt(dx**2 + dy**2)

        branch1 = (branch_length*(dy/vector_length - dx/vector_length), -branch_length*(dx/vector_length + dy/vector_length)) 
        branch2 = (-branch_length*(dy/vector_length + dx/vector_length), branch_length*(dx/vector_length - dy/vector_length))

        origin_point = [self.coord3d2d(origin)[0], self.coord3d2d(origin)[1]]

        x_component = origin_point[0] + dx
        y_component = origin_point[1] + dy
        triangle = [self.convert((x_component, y_component), 1), self.convert((x_component + branch1[0], y_component + branch1[1]), 1), self.convert((x_component + branch2[0], y_component + branch2[1]), 1)]
        pygame.draw.line(screen, color, self.convert((origin_point[0], origin_point[1]), 1), self.convert((x_component, y_component), 1), stroke)
        pygame.gfxdraw.filled_polygon(screen, triangle, color)

    def vector_field(self, vect_func, xyz_limits, dist, color=(0, 255, 0), branch_length=0.01):
        x = xyz_limits[0]
        while x <= xyz_limits[1]:
            y = xyz_limits[2]
            while y <= xyz_limits[3]:
                z = xyz_limits[4]
                while z <= xyz_limits[5]:
                    self.vector(vect_func(x, y, z), color, (x, y, z), 2, branch_length=branch_length)
                    z += dist
                y += dist
            x += dist

    def three_dimensional_space(self, scale=6):
        self.vector([2*scale, 0, 0], (255, 255, 255), [-scale, 0, 0], 2)
        self.vector([0, 2*scale, 0], (255, 255, 255), [0, -scale, 0], 2)
        self.vector([0, 0, 2*scale], (255, 255, 255), [0, 0, -scale], 2)

    def parametric_line(self, func, l_min, l_max, color=(255, 255, 0), dl=0.1, stroke=1):
        l = l_min
        line_points = []
        while l <= l_max:
            line_points.append(self.convert(self.coord3d2d(func(l)), 1))
            l += dl

        pygame.draw.lines(screen, color, False, line_points, 3)

    def parametric_surface(self, func, uv_limits, color=(0, 0, 200, 100), du=0.6, dv=0.6):
        polygons = []
        x = uv_limits[0]
        while x < uv_limits[1]:
            y = uv_limits[2]
            while y < uv_limits[3]:
                ds = []
                for i in range(0, 2):
                    for j in range(0 + 1*i, 2 - 3*i, 1 -2*i):
                        ds.append(self.convert(self.coord3d2d(func(x + i*du, y + j*dv)) , 1))
                
                polygons.append(ds)
                y += dv
            x += du
         
        for ds in polygons:
            pygame.gfxdraw.filled_polygon(screen, ds, color)

    def function(self, func, xy_limits, color=(0, 0, 200, 100), dx=0.6, dy=0.6):
        polygons = []
        x = xy_limits[0]
        while x < xy_limits[1]:
            y = xy_limits[2]
            while y < xy_limits[3]:
                ds = []
                for i in range(0, 2):
                    for j in range(0 + 1*i, 2 - 3*i, 1 -2*i):
                        ds.append(self.convert(self.coord3d2d([x + i*dx, y + j*dy, func(x + i*dx, y + j*dy)]) , 1))
                
                polygons.append(ds)
                y += dy
            x += dx
         
        for ds in polygons:
            pygame.gfxdraw.filled_polygon(screen, ds, color)

    def differential(self, func, init_c, t_max, color=(255, 255, 0), dt=0.01):
        point_list = []

        time = 0
        new_c = init_c
        while time <= t_max:
            dxyz = func(new_c)
            if len(point_list) == 0:
                point_list.append(self.convert(self.coord3d2d(new_c), 1))

            for i in range(0, 3):
                new_c[i] += dxyz[i] * dt

            point_list.append(self.convert(self.coord3d2d(new_c), 1))
            time += dt

        pygame.draw.circle(screen, color, [round(axie) for axie in self.convert(self.coord3d2d(new_c), 1)], 4)
        pygame.draw.lines(screen, color, False, point_list, 3)
  
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