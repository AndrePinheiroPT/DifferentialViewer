from Matiklib.math_tools import BLUE, ORANGE, YELLOW, Graph, Viewer
from math import * 

viewer = Viewer()
plot1 = Graph(viewer)

input_points = [
    [4, 1] # alpha
]

def rotate_square():
    alpha = input_points[0][1] - 1

    square = [
        (2*cos(pi/4 + alpha), 5 + 2*sin(pi/4 + alpha)),
        (2*cos(3*pi/4 + alpha), 5 + 2*sin(3*pi/4 + alpha)),
        (2*cos(5*pi/4 + alpha), 5 + 2*sin(5*pi/4 + alpha)),
        (2*cos(7*pi/4 + alpha), 5 + 2*sin(7*pi/4 + alpha))
    ]

    plot1.cartesian_plane()
    plot1.manipulation_points(input_points, (5, 5, 5, 5))
    input_points[0][0] = 4
    plot1.dot(input_points[0], ORANGE)
    plot1.line((4, 1), input_points[0], ORANGE, **{'stoke': 2})
    plot1.vector((cos(alpha), sin(alpha)), ORANGE, (0, 5))
    plot1.parametric_functions(lambda t: [0.5*cos(t), 5 + 0.5*sin(t)], 0, alpha, ORANGE)
    plot1.real_functions(lambda x: 2*(abs(sin(x)) + abs(cos(x))), 0, alpha, BLUE)

    x_square = [p[0] for p in square]
    plot1.line((sorted(x_square)[0], 0), (sorted(x_square)[3], 0), BLUE, **{'stoke': 4})
    plot1.line((sorted(x_square)[0], 0), (sorted(x_square)[0], 9), BLUE)
    plot1.line((sorted(x_square)[3], 0), (sorted(x_square)[3], 9), BLUE)


    for k in range(0, 3):
        plot1.line(square[k], square[k+1 if k <= 3 else k], **{'stroke': 4})
    plot1.line(square[0], square[3], YELLOW, **{'stroke': 4})

viewer.set_slides([rotate_square])
viewer.init()