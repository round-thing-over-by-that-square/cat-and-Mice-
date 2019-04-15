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
        self.coords = [float(int(W/2)), float(int(H - H/5))]
        self.target = 0
        self.sprite = arcade.Sprite("images/cat.png", .2)
        self.wanderDestination = [[-1, -1], 'x']

    
    def setWanderDestination(self, coords, direction):
        self.wanderDestination = [coords, direction]

    def getWanderDestination(self):
        return self.wanderDestination

    def getCoords(self):
        return self.coords

    def setCoords(self, coords):
        self.coords = coords

    def setTarget(self, mouse):
        self.target = mouse

    def getTarget(self):
        return self.target

    def draw(self):
        self.sprite.center_x = self.coords[0]
        self.sprite.center_y = self.coords[1]
        self.sprite.draw()
        #arcade.draw_circle_filled(self.coords[0], self.coords[1], float(int(W/50)), arcade.color.RED_DEVIL)
    
    def move(self, xDist, yDist):
        self.coords[0] = self.coords[0] + xDist
        self.coords[1] = self.coords[1] + yDist

     