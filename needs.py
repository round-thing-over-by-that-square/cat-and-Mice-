#Alex Lewandowski
#Cat and Mice
#Needs class

import arcade

class Need:
    def __init__(self, needType, coords, sprite):
        self.sprite = sprite
        self.type = needType
        self.coords = coords
        self.sprite.center_x = coords[0]
        self.sprite.center_y = coords[1]
        
    def draw(self):
        self.sprite.draw()

    def getSprite(self):
        return self.sprite

   # def draw(self):
