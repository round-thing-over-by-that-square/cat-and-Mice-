#Alex Lewandowski
#Cat and Mice
#Mouse Class
import arcade
import random
import time
from board import W
from board import H

TRAITS = ["00", "01", "10", "11"]

class Mouse:

    def __init__(self):
        self.age = 0
        self.time = 0
        self.coords = [random.randrange(0, W), random.randrange(0, H)]

        # 1 = eat, 2 = drink, 3 = reproduce, 4 = flee
        self.needState = random.choice([1,2,3,4])

        #self.chromosome = strength + smellType + speed + metabolicRate + size + smallSpacePrefLevel + catFear
        self.chromosome = random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS)

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome

    ### Gene Getters ###
    def getCoords(self):
        return self.coords

    def getSmellStrength(self):
        return self.chromosome[0:2]

    def getSmellType(self):
        return self.chromosome[2:4]

    def getSpeed(self):
        return self.chromosome[4:6]

    def getMetabolicRate(self):
        return self.chromosome[6:8]

    def getSize(self):
        return self.chromosome[8:10]

    def smallSpacePrefLevel(self):
        return self.chromosome[10:12]

    def catFear(self):
        return self.chromosome[12:14]

    def draw(self):
        arcade.draw_circle_filled(self.coords[0], self.coords[1], float(int(W/100)), arcade.color.LIGHT_BROWN)  

        

        

    