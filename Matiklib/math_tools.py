import pygame
import pygame.gfxdraw
from pygame.locals import *
from math import *

# Screen configuration
CONFIG = {
    'screen_width': 700,
    'screen_height': 700
}

# Colors 
CYAN = (55, 55, 55)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
BLUE = (0, 96, 255)

# screen and font variables. They value is none until pygame run
screen = None
font = None

class Viewer():
    def __init__(self, **kwargs):
        '''
        Viewer is a heart class. This class make possible run pygame, to manage the
        surfaces, slides and send information to the other classes
        '''
        global CONFIG
        self.mouse_pressed = False
        self.mouse_state = []
        self.surfaces = [] # This is a list of 2 pairs: pygame surface object and his coords
        self.slides = []
        self.slide_index = 0

        for key, value in kwargs.items():
            CONFIG.update({key: value})
        self.time = 0
    
    def set_slides(self, slides):
        '''
        set_slides defines a new list of slides
        :slides: a list of functions (slides)
        '''
        self.slides = slides

    def update_config(self, config):
        '''
        update_cofing defines a new screen configuration
        :slides: configuration of screen using dictionary 
        '''
        CONFIG.update(config)

    def init(self):
        '''
        init is the main method of the class. When called, the program starts.
        Also it's important to have defined the slides list before the method being called.
        '''
        global screen, font, CONFIG
        pygame.init()

        # setup of variables
        screen = pygame.display.set_mode((CONFIG['screen_width'], CONFIG['screen_height']))
        pygame.display.set_caption('Matik')
        pygame.Surface((CONFIG['screen_width'], CONFIG['screen_height']))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 15)
        clock = pygame.time.Clock()
        
        while True:
            # 60 fps
            clock.tick(60)
            # clean the screen and the surfaces
            screen.fill((0, 0, 0))
            for surf in self.surfaces:
                surf[0].fill((0, 0, 0))
                screen.blit(*surf)

            # set mouse coords and run the slide defined by his index
            self.mouse_state = pygame.mouse.get_pos()
            self.slides[self.slide_index]()
            
            for event in pygame.event.get():
                # close the window
                if event.type == QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    # Change the slide index through keyboard, using the left and right arrow.
                    if event.key == pygame.K_LEFT:
                        if self.slide_index >= 1:
                            self.slide_index -= 1
                            self.time = 0

                    if event.key == pygame.K_RIGHT:
                        if self.slide_index < len(self.slides) - 1:
                            self.slide_index += 1
                            self.time = 0

                # Set the state of mouse (pressed or not pressed)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pressed = False

            # show the surfaces on screen
            for surf in self.surfaces:
                screen.blit(*surf)
            
            # update surfaces and creen
            pygame.display.update()
            pygame.display.flip()
            self.time += 0.1

class Graph:
    def __init__(self, viewer, **kwargs):
        '''
        Graph class is used to plot interactive graphs. It allows to plot: a cartesian plane;
        vector fields; vectors; parametric curves; functions; complex functions; linear transformations and a bit more.

        :viewer: class used for extract information of mouse.
        :kwargs: dictionary with the surface configuration.
        '''
        graph_config = {
            'coords': (0, 0),
            'width': CONFIG['screen_width'],
            'height': CONFIG['screen_height'],
            'unit_x': 60,
            'unit_y': 60,
            'x_label': 'X',
            'y_label': 'Y'
        }
        for key, value in kwargs.items():
            graph_config.update({key: value})
        
        # setup surface
        self.surface = pygame.Surface([graph_config['width'], graph_config['height']])
        self.viewer = viewer
        self.viewer.surfaces.append([self.surface, graph_config['coords']])

        # variable setting
        self.coords = graph_config['coords']
        self.width = graph_config['width']
        self.height = graph_config['height']
        self.unit_x = graph_config['unit_x']
        self.unit_y = graph_config['unit_y']
        self.x_label = graph_config['x_label']
        self.y_label = graph_config['y_label']
        self.prev_state = None
        self.object_selected = None
    
        self.origin = [self.width/2, self.height/2]      

    def check_mouse(self):
        '''
        check_mouse is used to manipulate the cartesian plane. It defines a 
        new origin coords by pressed mouse movement.
        '''
        mouse_state = pygame.mouse.get_pos()
        
        if self.viewer.mouse_pressed:
            if self.coords[0] <= mouse_state[0] <= self.coords[0] + self.width and self.coords[1] <= mouse_state[1] <= self.coords[1] + self.height:
                if self.prev_state == None:
                    self.prev_state = mouse_state
                self.origin[0] += -(self.prev_state[0] - mouse_state[0])*.5
                self.origin[1] += -(self.prev_state[1] - mouse_state[1])*.5
                self.prev_state = mouse_state
        else:
            self.prev_state = None

    def manipulation_points(self, points_list, hitbox):
        '''
        manipulation_points does a new list of points based on mouse coords. A click
        on one point of the list allows to change his coords
        :points_list: a list of points which can be manipulated
        :hitbox: area where mouse click need to be contained
        '''
        points = points_list
        if self.object_selected == None:
            for key, point in enumerate(points):
                # check if mouse is contained in hitbox
                if (self.convert_to_pygame(*point)[0] - hitbox[0] <= self.viewer.mouse_state[0] <= self.convert_to_pygame(*point)[0] + hitbox[2]) and (self.convert_to_pygame(*point)[1] - hitbox[1] <= self.viewer.mouse_state[1] <= self.convert_to_pygame(*point)[1] + hitbox[3]) and self.viewer.mouse_pressed:
                    self.object_selected = key
                    # change the coords 
                    points[key] = self.convert_to_xOy(*self.viewer.mouse_state)
                    break
        elif self.viewer.mouse_pressed:
            points_list[self.object_selected] = self.convert_to_xOy(*self.viewer.mouse_state)
        else:
            self.object_selected = None
        return points_list

    def convert_to_pygame(self, x, y):
        '''
        Convert the cartesian plane coords to the pygame coords
        :x: x-axis
        :y: y-axis
        '''
        return [x*self.unit_x + self.origin[0], -y*self.unit_x + self.origin[1]]

    def convert_to_xOy(self, x, y):
        '''
        Convert the pygame coords to the cartesian plane coords
        :x: x of screen
        :y: y of screen
        '''
        return [(x - self.origin[0])/self.unit_y, -(y - self.origin[1])/self.unit_y]

    def cartesian_plane(self, move_grid=True, **kwargs):
        '''
        cartesian_plane plots a xOy plane on the surface.
        :move_grid: allows you create a interactive plane or not
        :kwargs: additional information
        '''
        config = {
            'color': WHITE,
            'stroke': 1
        }
        for key, value in kwargs.items():
            config.update({key: value})

        # use check_mouse() to move the grid
        if move_grid and self.object_selected == None:
            self.check_mouse()

        # plot lines and values in positive direction of x
        x = self.origin[0]
        x_value = 0
        while x <= self.width: 
            pygame.draw.line(self.surface, CYAN, (x, 0), (x, self.height), config['stroke'])
            self.surface.blit(font.render(f'{x_value}', False, config['color']), (x + 2 , self.origin[1]))
            x += self.unit_x
            x_value += 1
        
        # plot lines and values in negative direction of x
        x = self.origin[0]
        x_value = 0
        while x >= 0:
            pygame.draw.line(self.surface, CYAN, (x, 0), (x, self.height), config['stroke'])
            self.surface.blit(font.render(f'{x_value}', False, config['color']), (x + 2 , self.origin[1]))
            x -= self.unit_x
            x_value -= 1

        # plot lines and values in negative direction of y
        y = self.origin[1]
        y_value = 0
        while y <= self.height:
            pygame.draw.line(self.surface, CYAN, (0, y), (self.width, y), config['stroke'])
            if y_value != 0:
                self.surface.blit(font.render(f'{y_value}', False, config['color']), (self.origin[0]+2, y-14))
            y += self.unit_y
            y_value -= 1

        # plot lines and values in positive direction of y
        y = self.origin[1]
        y_value = 0
        while y >= 0:
            pygame.draw.line(self.surface, CYAN, (0, y), (self.width, y), config['stroke'])
            if y_value != 0:
                self.surface.blit(font.render(f'{y_value:.1f}', False, config['color']), (self.origin[0]+2, y-14))
            y -= self.unit_y
            y_value += 1
        
        # plot the label of each axis and the main line of each one
        self.surface.blit(font.render(f'{self.x_label}', False, config['color']), (self.width-10, self.origin[1]-14))
        self.surface.blit(font.render(f'{self.y_label}', False, config['color']), (self.origin[0]-12, 0))
        pygame.draw.line(self.surface, config['color'], (self.origin[0], 0), (self.origin[0], self.height), config['stroke'])
        pygame.draw.line(self.surface, config['color'], (0, self.origin[1]), (self.width, self.origin[1]), config['stroke'])

    def linear_transformation(self, matrix, color=YELLOW, **kwargs):
        '''
        linear_transformation plots a grid of a linear transformation done by a 2x2 matrix 
        :matrix: 2D list with the values 
        :color: color of the grid
        :kwargs: additional information
        '''
        config = {
            'stroke': 1
        }
        for key, value in kwargs.items():
            config.update({key: value})
        
        # seting the slope values
        alpha = matrix[1][0]/(0.001 if matrix[0][0] == 0 else matrix[0][0])
        beta = matrix[1][1]/(0.001 if matrix[0][1] == 0 else matrix[0][1])

        # plot lines in x and y positive direction
        x = self.origin[0]
        while x <= self.width + 5*self.unit_x: 
            pygame.draw.line(self.surface, color, (x - (self.height - self.origin[1])/alpha, self.height), (x + self.origin[1]/alpha, 0), config['stroke'])
            pygame.draw.line(self.surface, color, (x - (self.height - self.origin[1])/beta, self.height), (x + self.origin[1]/beta, 0), config['stroke'])
            x += self.unit_x
        
        # plot lines in x and y negative direction
        x = self.origin[0]
        while x >= 0 - 5*self.unit_x:
            pygame.draw.line(self.surface, color, (x - (self.height - self.origin[1])/alpha, self.height), (x + self.origin[1]/alpha, 0), config['stroke'])
            pygame.draw.line(self.surface, color, (x - (self.height - self.origin[1])/beta, self.height), (x + self.origin[1]/beta, 0), config['stroke'])
            x -= self.unit_x

    def real_functions(self, function, xd_min, xd_max, color=YELLOW, dx=0.01, **kwargs):
        '''
        real_functions plots a function on xOy plane. So it's R -> R function.
        :function: function with has x as parameter and returns f(x) value
        :xd_min: lowest value of the domain
        :xd_max: highest value of the domain
        :color: color of the function
        :dx: discrete value interval (delta x)
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})

        # get the lowest value for starting plot
        x = xd_min if xd_min <= xd_max else xd_max
        # add initil point to the points list
        function_points = []
        function_points.append(self.convert_to_pygame(x, function(x)))
        # loop for get more points.
        while x <= (xd_max if xd_min < xd_max else xd_min):
            x += dx
            y = function(x)
            function_points.append(self.convert_to_pygame(x, y))

        if len(function_points) >= 2:
            # draw the function on surface
            pygame.draw.lines(self.surface, color, False, function_points, config['stroke'])

    def complex_functions(self, func, domain_func, t_min, t_max, color=YELLOW, dt=0.01, **kwargs):
        '''
        complex_functions plots a function on complex plane. So it's R^2 -> R^2 function.
        The domain function is a parametric line used to get the values on complex plane.
        :func: function with has a and b as parameter (a+ib) and returns a list which represents a complex value [a, b]
        :domain_func: parametric curve that represents the domain of the function. So it's R -> R^2 function
        :t_min: lowest value of the domain of parametric curve
        :t_max: highest value of the domain of parametric curve
        :color: color of the function
        :dx: discrete value interval (delta x)
        :kwargs: additional information
        '''
        config = {
            'stroke': 2
        }
        for key, value in kwargs.items():
            config.update({key: value})
        
        # get the lowest value of t for starting plot
        complex_function_points = []
        t = t_min if t_min <= t_max else t_max
        while t <= (t_max if t_min < t_max else t_min):
            t += dt
            z = []
            for i in range(0, 2):
                z.append(func(*domain_func(t))[i])

            complex_function_points.append(self.convert_to_pygame(z[0], z[1]))

        if len(complex_function_points) >= 2:
            pygame.draw.lines(self.surface, color, False, complex_function_points, config['stroke'])

    def derivative_line(self, func, x, range_line, color=PINK, h=0.0001, **kwargs):
        '''
        derivative_line returns the value of the slope in some point of a real function and plots a tangent line in that point.
        :func: real function R -> R
        :x: x value used to get a point
        :range_line: length of the line that will be plotted
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})

        # compute the derivative
        derivative = (func(x+h) - func(x)) / h  # slope
        b = func(x) - derivative*x

        # plot the tangent line
        if range_line != 0:
            x_range = range_line/(1+derivative**2)**0.5
            pygame.draw.line(self.surface, color, 
            self.convert_to_pygame(x - x_range, (x - x_range)*derivative + b), 
            self.convert_to_pygame(x + x_range, (x + x_range)*derivative + b), config['stroke'])
            
        return derivative

    def riemann_rectangles(self, func, x_min, x_max, n, color_init=[131, 47, 0, 200], color_end=[231, 242, 0, 200]):
        '''
        riemann_rectangles plot rectangles under the curve of a real function (R->R) and return the 
        area of them. 
        :func: real function R -> R
        :x_min: boundary a
        :x_max: boundary b
        :n: number of rectangles
        :color_init: intial color of the gradient
        :color_end: end color of the gradient
        '''

        # set color gradient (delta color)
        color = [0, 0, 0, 0]
        d_color = [0, 0, 0, 0]
        for k in range(0, 4):
            d_color[k] = (color_end[k] - color_init[k]) / n

        # descrite value
        dx = (x_max - x_min) / n
        total_sum = 0
        
        for i in range(0, n):
            for k in range(0, 4):
                color[k] = color_init[k] + d_color[k]*i
            x = x_min + i*dx
            dy = func(x)
            total_sum += dy*dx
            # plot each rectangle
            pygame.gfxdraw.box(self.surface, pygame.Rect(self.convert_to_pygame(x, func(x)), (dx*self.unit_x + 1, dy*self.unit_y + 2)), color)

        return total_sum

    def limit_aproximation(self, func, x, delta, color=ORANGE, **kwargs):
        '''
        limit_aproximation plots the boundary of aproximation and returns the lateral limits of the function.
        :func: real function R -> R
        :x: the value of aproximation
        :delta: sets the boundary of aproximation
        :color: color of the boundary
        :kwargs: additional information
        '''
        config = {
            'radius': 4
        }
        for key, value in kwargs.items():
            config.update({key: value})

        # plots the boundary
        self.real_functions(func, x - delta, x + delta, color=color)
        standard_limit = self.convert_to_pygame(x, func(x))
        for i in range(0, 2):
            standard_limit[i] = round(standard_limit[i])
        pygame.draw.circle(self.surface, color, standard_limit, config['radius'])

        # returns the lateral limits
        return [func(x - delta), func(x + delta)]

    def parametric_functions(self, func, t_min, t_max, color=YELLOW, dt=0.01, **kwargs):
        '''
        parametric_functions plots a function R->R^2.
        :func: real function R -> R^2
        :t_min: lowest value of the domain
        :t_max: highest value of the domain
        :color: color of the function
        :dt: discrete value interval (delta t)
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})

        # set lowest value
        t = t_min if t_min <= t_max else t_max
        # get all points of the function
        point_list = []
        point_list.append(self.convert_to_pygame(*func(t)))
        while t <= (t_max if t_min < t_max else t_min):
            point_list.append(self.convert_to_pygame(*func(t)))
            t += dt
        # plot function
        pygame.draw.lines(self.surface, color, False, point_list, config['stroke'])

    def bazier_curve(self, points_list, t_max, color=YELLOW, dt=0.01, **kwargs):
        '''
        bazier_curve plots a curve based on list of points.
        :points_list: list of points used for make the curve
        :t_max: goes from 0 to 1, 1 means a complete curve
        :color: color of the curve
        :dt: discrete value interval (delta t)
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})

        bezier_points = []
        # compute all points of the curve
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
            
            bezier_points.append(self.convert_to_pygame(*points[0]))
            t += dt
        
        # plots the curve
        pygame.draw.lines(self.surface, color, False, bezier_points, config['stroke'])
        
    def line(self, init_point, end_point, color=YELLOW, **kwargs):
        '''
        plots a line
        :init_point: initial point of the line
        :end_point: final point of the line
        :color: color of the line
        :kwargs: additional information
        '''
        config = {
            'stroke': 1
        }
        for key, value in kwargs.items():
            config.update({key: value})
        # plots the line
        pygame.draw.line(self.surface, color, self.convert_to_pygame(*init_point), self.convert_to_pygame(*end_point), config['stroke'])

    def dot(self, coords, color=YELLOW, **kwargs):
        '''
        plots a dot
        :coords: coords of the point
        :color: color of the dot
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})
        # plots the dot
        integer_coords = [round(self.convert_to_pygame(*coords)[0]), round(self.convert_to_pygame(*coords)[1])]
        pygame.draw.circle(self.surface, color, integer_coords, 5)

    def circle(self, coords, radius, color=YELLOW, **kwargs):
        '''
        plots a circle
        :coords: coords of the center of circle
        :color: color of the circle
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})
        # plots the circle
        integer_coords = [round(self.convert_to_pygame(*coords)[0]), round(self.convert_to_pygame(*coords)[1])]
        pygame.draw.circle(self.surface, color, integer_coords, radius, config['stroke'])

    def polygon(self, points_list, color=YELLOW, **kwargs):
        '''
        plots a polygon based on points 
        :points_list: list of points used for draw the polygon
        :color: color of the circle
        :kwargs: additional information
        '''
        config = {
            'stroke': 3
        }
        for key, value in kwargs.items():
            config.update({key: value})
        # set points list
        standard_points = []
        for point in points_list:
            standard_points.append(self.convert_to_pygame(*point))
        # plots polygon
        pygame.draw.polygon(self.surface, color, standard_points, config['stroke'])

    def vector(self, vect, color, origin=[0, 0], **kwargs):
        '''
        plots a vector
        :vect: coords of the vector
        :color: color of the vector
        :origin: origin coords of the vector 
        :kwargs: additional information
        '''
        config = {
            'stroke': 4,
            'angle': pi/7,
            'arrow_length': 0.25
        }
        for key, value in kwargs.items():
            config.update({key: value})
        # define the unit vector of the vector
        vector_length = 0.001 if sqrt(vect[0]**2 + vect[1]**2) == 0 else sqrt(vect[0]**2 + vect[1]**2)
        unit_vector = [-vect[0]/vector_length, -vect[1]/vector_length]

        # set the branches of the vector
        theta = config['angle']
        vector_angle = (2*pi - acos(unit_vector[0]) if unit_vector[1] <= 0 else acos(unit_vector[0]))

        branch1 = [config['arrow_length']*cos(vector_angle - theta), config['arrow_length']*sin(vector_angle - theta)]
        branch2 = [config['arrow_length']*cos(vector_angle + theta), config['arrow_length']*sin(vector_angle + theta)]

        # plots the vector
        x_component = origin[0] + vect[0]
        y_component = origin[1] + vect[1]
        triangle = [self.convert_to_pygame(x_component, y_component), self.convert_to_pygame(x_component + branch1[0], y_component + branch1[1]), self.convert_to_pygame(x_component + branch2[0], y_component + branch2[1])]
        pygame.draw.line(self.surface, color, self.convert_to_pygame(origin[0], origin[1]), self.convert_to_pygame(x_component, y_component), config['stroke'])
        pygame.gfxdraw.filled_polygon(self.surface, triangle, color)

    def __vector_render(self, vect_func, x, y):
        
        vx = vect_func(x, y)[0]
        vy = vect_func(x, y)[1]

        # set color gradient according to norm of the vector
        t = sqrt(vx**2 + vy**2)/50 if sqrt(vx**2 + vy**2)/50 <= 1 else 1
        h = t*510 if t <= 0.5 else 255
        q = 255 if t <= 0.5 else (-t*510 + 510)

        return [
            vx/(0.01 if sqrt(vx**2 + vy**2) == 0 else sqrt(vx**2 + vy**2)), 
            vy/(0.01 if sqrt(vx**2 + vy**2) == 0 else sqrt(vx**2 + vy**2)),
            [h, q, 0]
        ]

    def vector_field(self, vect_func, **kwargs):
        '''
        plots a vector field
        :vect_function: real function R^2->R^2 
        '''

        # get positive values in x direction
        x = self.origin[0]
        x_value = 0
        while x <= CONFIG['screen_width'] + self.unit_x:
            # plot vectors in y positive direction
            y = self.origin[1]
            y_value = 0
            while y <= CONFIG['screen_height'] + self.unit_y:
                if y_value != 0:
                    self.vector(self.__vector_render(vect_func, x_value, y_value)[:2], self.__vector_render(vect_func, x_value, y_value)[2], (x_value, y_value), **kwargs)
                y += self.unit_y
                y_value -= 1

            # plot vectors in y negative direction
            y = self.origin[1]
            y_value = 0
            while y >= 0 - self.unit_y:
                self.vector(self.__vector_render(vect_func, x_value, y_value)[:2], self.__vector_render(vect_func, x_value, y_value)[2], (x_value, y_value), **kwargs)
                y -= self.unit_y
                y_value += 1

            x += self.unit_x
            x_value += 1
        
        # get negative values in x direction
        x = self.origin[0]
        x_value = 0
        while x >= 0 - self.unit_x:
            # plot vectors in y positive direction
            y = self.origin[1]
            y_value = 0
            while y <= CONFIG['screen_height'] + self.unit_y:
                if y_value != 0:
                    self.vector(self.__vector_render(vect_func, x_value, y_value)[:2], self.__vector_render(vect_func, x_value, y_value)[2], (x_value, y_value), **kwargs)
                y += self.unit_y
                y_value -= 1

            # plot vectors in y negative direction
            y = self.origin[1]
            y_value = 0
            while y >= 0 - self.unit_y:
                self.vector(self.__vector_render(vect_func, x_value, y_value)[:2], self.__vector_render(vect_func, x_value, y_value)[2], (x_value, y_value), **kwargs)
                y -= self.unit_y
                y_value += 1
            x -= self.unit_x
            x_value -= 1

class Scense3D:
    def __init__(self, r, theta, phi, viewer):
        self.r = r
        self.theta = theta
        self.phi = phi 
        self.can_change = False
        self.prev_state = None
        self.viewer = viewer
        self.dxy = [0, 0]

        self.h = 0.5
        self.r = 0.25

    def __cone(self, u, v):
        return [(self.r*u/self.h)*cos(v), (self.r*u/self.h)*sin(v), u]

    def __vector_render(self, vect_func, x, y, z):
        
        vx = vect_func(x, y, z)[0]
        vy = vect_func(x, y, z)[1]
        vz = vect_func(x, y, z)[2]
        norm = (0.01 if sqrt(vx**2 + vy**2 + vz**2) == 0 else sqrt(vx**2 + vy**2 + vz**2))

        t = sqrt(vx**2 + vy**2 + vz**2)/50 if sqrt(vx**2 + vy**2 + vz**2)/50 <= 1 else 1
        h = t*510 if t <= 0.5 else 255
        q = 255 if t <= 0.5 else (-t*510 + 510)

        return [2*vx/norm, 2*vy/norm, 2*vz/norm, [h, q, 0]]

    def t3d_to_2d(self, point):
        self.check_mouse()
        matrix = (
            ((1/self.r)*sin(self.phi), (1/self.r)*cos(self.phi), 0),
            (-(1/self.r)*cos(self.phi)*cos(self.theta), (1/self.r)*sin(self.phi)*cos(self.theta), (1/self.r)*sin(self.theta)),
            (0, 0, 0)
        )
        
        new_point = [0, 0]
        for k in range(0, 2):
            for i in range(0, 3):
                new_point[k] += matrix[k][i]*point[i]
                
        return new_point

    def convert(self, coords, standard=True):
        if standard:
            return [coords[0]*10 + CONFIG['screen_width']/2, -coords[1]*10 + CONFIG['screen_height']/2]
        else:
            return [(coords[0] - CONFIG['screen_width']/2)/10,-(coords[1] - CONFIG['screen_height']/2)/10]

    def check_mouse(self):
        mouse_state = self.convert(pygame.mouse.get_pos(), 0)
        if self.viewer.mouse_pressed:
            if not self.can_change:
                self.prev_state = mouse_state
            self.theta = self.dxy[0] + (mouse_state[1] - self.prev_state[1])*0.10
            self.phi = self.dxy[1] + (mouse_state[0] - self.prev_state[0])*0.10
            self.can_change = True
        else:
            if self.can_change:
                self.dxy = [self.theta, self.phi]
            self.can_change = False
            
    def vector(self, vect, color, origin=(0, 0, 0), **kwargs):
        config = {
            'stroke': 3,
            'h': 0.5,
            'r': 0.25
        }
        for key, value in kwargs.items():
            config.update({key: value})

        self.h = config['h']
        self.r = config['r']

        norm = sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)

        theta = acos(vect[2]/(0.001 if norm == 0 else norm))*(-1 if vect[0] < 0 else 1)  -pi
        phi = pi/2 + atan(vect[1]/(0.001 if vect[0] == 0 else vect[0]))
        trans_vect = [origin[i] + vect[i] for i in range(0, 3)]

        self.parametric_surface(self.__cone, [0, self.h, 0, 2*pi], (*color, 250), **{'rotation': (theta, phi), 'translation': trans_vect})

        dx = self.t3d_to_2d(vect)[0]
        dy = self.t3d_to_2d(vect)[1]

        origin_point = [self.t3d_to_2d(origin)[0], self.t3d_to_2d(origin)[1]]

        x_component = origin_point[0] + dx
        y_component = origin_point[1] + dy
        pygame.draw.line(screen, color, self.convert((origin_point[0], origin_point[1]), 1), self.convert((x_component, y_component), 1), config['stroke'])

    def vector_field(self, vect_func, **kwargs):
        config = {
            'stroke': 3,
            'h': 0.5,
            'r': 0.25,
            'dist': 4,
            'xyz_limits': [-5, 5, -5, 5, -5, 5]
        }
        for key, value in kwargs.items():
            config.update({key: value})

        x = config['xyz_limits'][0]
        while x <= config['xyz_limits'][1]:
            y = config['xyz_limits'][2]
            while y <= config['xyz_limits'][3]:
                z = config['xyz_limits'][4]
                while z <= config['xyz_limits'][5]:
                    vect_row = self.__vector_render(vect_func, x, y, z)
                    self.vector(vect_row[:3], vect_row[3], (x, y, z), **config)
                    z += config['dist']
                y += config['dist']
            x += config['dist']

    def cartesian_plane3D(self, scale=4, **kwargs):
        config = {
            'stroke': 2,
            'h': 0.5,
            'r': 0.25,
            'color_vect': WHITE
        }
        for key, value in kwargs.items():
            config.update({key: value})

        for k in range(-3, 4):
            self.parametric_line(lambda t: (k, -0.2+t, 0), 0, 0.4, config['color_vect'], **config)
            self.parametric_line(lambda t: (-0.2+t, k, 0), 0, 0.4, config['color_vect'], **config)
            self.parametric_line(lambda t: (0, -0.2+t, k), 0, 0.4, config['color_vect'], **config)
        self.vector([2*scale, 0, 0], config['color_vect'], [-scale, 0, 0], **config)
        self.vector([0, 2*scale, 0], config['color_vect'], [0, -scale, 0], **config)
        self.vector([0, 0, 2*scale], config['color_vect'], [0, 0, -scale], **config)

    def parametric_line(self, func, l_min, l_max, color=YELLOW, dl=0.1, **kwargs):
        config = {
            'stroke': 3,
        }
        for key, value in kwargs.items():
            config.update({key: value})

        l = l_min
        line_points = []
        while l <= l_max:
            line_points.append(self.convert(self.t3d_to_2d(func(l)), 1))
            l += dl

        pygame.draw.lines(screen, color, False, line_points, config['stroke'])

    def parametric_surface(self, func, uv_limits, color=(0, 0, 200, 100), du=0.6, dv=0.6, **kwargs):
        config = {
            'rotation': (0, 0),
            'translation': (0, 0, 0)
        }
        for key, value in kwargs.items():
            config.update({key: value})

        polygons = []
        x = uv_limits[0]
        while x < uv_limits[1]:
            y = uv_limits[2]
            while y < uv_limits[3]:
                ds = []
                for i in range(0, 2):
                    for j in range(0 + 1*i, 2 - 3*i, 1 -2*i):
                        output = func(x + i*du, y + j*dv)
                        new_output = [
                            config['translation'][0] + output[0]*cos(config['rotation'][1]) - (output[1]*cos(config['rotation'][0]) - output[2]*sin(config['rotation'][0]))*sin(config['rotation'][1]),
                            config['translation'][1] + (output[1]*cos(config['rotation'][0]) - output[2]*sin(config['rotation'][0]))*cos(config['rotation'][1]) + output[0]*sin(config['rotation'][1]),
                            config['translation'][2] + output[2]*cos(config['rotation'][0]) + output[1]*sin(config['rotation'][0])
                        ]
                        ds.append(self.convert(self.t3d_to_2d(new_output) , 1))
                
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
                        ds.append(self.convert(self.t3d_to_2d([x + i*dx, y + j*dy, func(x + i*dx, y + j*dy)]) , 1))
                
                polygons.append(ds)
                y += dy
            x += dx
         
        for ds in polygons:
            pygame.gfxdraw.filled_polygon(screen, ds, color)

    def differential(self, func, init_c, t_max, color=YELLOW, dt=0.01, **kwargs):
        config = {
            'stroke': 3,
        }
        for key, value in kwargs.items():
            config.update({key: value})

        point_list = []

        time = 0
        new_c = init_c
        while time <= t_max:
            dxyz = func(new_c)
            if len(point_list) == 0:
                point_list.append(self.convert(self.t3d_to_2d(new_c), 1))

            for i in range(0, 3):
                new_c[i] += dxyz[i] * dt

            point_list.append(self.convert(self.t3d_to_2d(new_c), 1))
            time += dt

        pygame.draw.circle(screen, color, [round(axie) for axie in self.convert(self.t3d_to_2d(new_c), 1)], config['stroke'])
        pygame.draw.lines(screen, color, False, point_list, config['stroke'])
