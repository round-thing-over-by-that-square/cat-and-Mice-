#Alex Lewandowski   
#Obstacle Class

import arcade

class Obstacle:
    def __init__(self, sprite, centerCoords, radius):
        self.centerCoords = centerCoords
        self.sprite = sprite
        self.sprite.center_x = self.centerCoords[0] 
        self.sprite.center_y = self.centerCoords[1]
        self.radius = radius

    def getRadius(self):
        return self.radius

    def getCoords(self):
        return self.centerCoords
    
    def draw(self):
        self.sprite.draw()  