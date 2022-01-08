# Matik
Matik is an engine for programatic interactive plots, designed for understanding math concepts. The program was developed by André Pinheiro and took 5 months for its final version and to be available.

## Installation
Matik requires Puthon 3.7 or higher to be runned. The only 
library necessary to use Matik is pygame 1.9.

### Directly
```sh
# Install pygame first
pip install pygame
# After that, install the matik
pip install Matik
```
# Using Matik

After the installation, create a python file with the folling form.
```python
from Matiklib.math_tools import *

viewer = Viewer()
plot = Graph(viewer)

def my_first_plot():
    plot.cartesian_plane()
    plot.real_functions(lambda x: x**2, -3, 3)

viewer.set_slides([my_first_plot])
viewer.init()
```
Every Matik project has a class called Viewer, this class is necessary for run pygame and the entire library. 

There are two mainly classes: ```Graph``` and ```Graph3D```. It's obrigatory pass the class viewer as a parameter of these two classes.

The function ```my_first_plot``` is called *slide*. A slide is a group of commands used to plot math objects and it's necessary to add into viewer using ```viewer.set_slides()``` with a list of slides.

And finally, for the program starts we call ```viewer.init()```.

# Contributing
Is always welcome. Please explain the motivation for a given change and examples of its effect.

# License
This project falls under the MIT license.


