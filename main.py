from Matiklib.math_tools import *

CONFIG = {'screen_width': 800, 'screen_height': 600}
viewer = Viewer(**CONFIG)
grafic1 = Graph(viewer)
tools3D = Scense3D(10, 0, 0, viewer)

time = 0


def minigrath_test():
    grafic1.cartesian_plane()

viewer.set_slides([minigrath_test])
viewer.init()

