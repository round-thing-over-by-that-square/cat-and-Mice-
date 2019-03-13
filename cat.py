#Alex Lewandowski
#Cat and Mice
#Cat Class
import arcade
import random
import time
from board import W
from board import H

class Cat:

    def __init__(self):
        self.age = 0
        self.time = 0
        self.coords = [W/2, H/2]

    def getCoords(self):
        return self.coords
     