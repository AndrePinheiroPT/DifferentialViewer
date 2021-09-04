import sys
sys.path.insert(0, '/home/pi/Documents/GitProjects/DifferentialViewer/graph_tools')

from math_tools import *
from math import *


class Scene:
    def __init__(self, mouse_state):
        self.mouse_state = mouse_state

    def __new__(self, mouse_state):
        return [self.global_slide, self.slide1, self.slide2, self.slide3, self.slide4]

    def global_slide():
        cartesian_plane()

    def slide1(self):
        real_functions(lambda x: 1/x**2, 0.01, 6, color=(87, 0, 240))

    def slide2(self):
        real_functions(lambda x: 1/x**2, 0.01, 6, color=(87, 0, 240))
        derivative_line(lambda x: 1/x**2, self.mouse_state[0], 0.01, 6)

    def slide3(self):
        real_functions(lambda x: 1/x**2, 0.01, 6, color=(87, 0, 240))
        limit_aproximation(lambda x: 1/x**2, 3, 0.5)
        derivative_line(lambda x: 1/x**2, self.mouse_state[0], 0.01, 6)

    def slide4(self):
        real_functions(lambda x: 1/x**2, 0.01, 6, color=(87, 0, 240))
        riemann_rectangles(lambda x: 1/x**2, 1, 6, 1050)
        limit_aproximation(lambda x: 1/x**2, 3, 0.5)
        derivative_line(lambda x: 1/x**2, self.mouse_state[0], 0.01, 6)

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
        f_x = x**2 - y**2
        f_y = 2*x*y
        return [f_x, f_y]