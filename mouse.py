#Alex Lewandowski
#Cat and Mice
#Mouse Class
import arcade
import random
import time
from board import W
from board import H

TRAITS = ["00", "01", "10", "11"]

class Mouse(arcade.Sprite):

    def __init__(self):
        self.age = 0
        self.time = 0
        self.coords = [random.randrange(0, W), random.randrange(0, H)]
        self.spriteList = arcade.SpriteList()

        # 1 = eat, 2 = drink, 3 = reproduce, 4 = flee
        self.needState = random.choice([1,2,3,4])

        #self.chromosome = strength + smellType + speed + metabolicRate + size + smallSpacePrefLevel + catFear
        self.chromosome = random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS)

    def getCoords(self):
        return self.coords

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def getChromosome(self):
        return self.chromosome

    ### Gene Getters ###

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

    def getSmallSpacePrefLevel(self):
        return self.chromosome[10:12]

    def getCatFear(self):
        return self.chromosome[12:14]

    def draw(self):
        #handle size
        scale = 0
        if self.getSize() == "00":
            scale = 0.13
        elif self.getSize() == "01":
            scale = 0.17
        elif self.getSize() == "01":
            scale = 0.22
        else:
            scale = 0.26

        #handle smell type and strength
        smellAuraSprite = 0

        testSmellType = self.getSmellType()
        testSmellStrength = self.getSmellStrength()

        if self.getSmellType() == "00" and self.getSmellStrength() == "01":
            smellAuraSprite = arcade.Sprite("images/aura2_green.png", scale)
        elif self.getSmellType() == "00" and self.getSmellStrength() == "10":
            smellAuraSprite = arcade.Sprite("images/aura3_green.png", scale)
        elif self.getSmellType() == "00" and self.getSmellStrength() == "11":
            smellAuraSprite = arcade.Sprite("images/aura4_green.png", scale)
        
        elif self.getSmellType() == "01" and self.getSmellStrength() == "01":
            smellAuraSprite = arcade.Sprite("images/aura2_orange.png", scale)
        elif self.getSmellType() == "01" and self.getSmellStrength() == "10":
            smellAuraSprite = arcade.Sprite("images/aura3_orange.png", scale)
        elif self.getSmellType() == "01" and self.getSmellStrength() == "11":
            smellAuraSprite = arcade.Sprite("images/aura4_orange.png", scale)

        elif self.getSmellType() == "10" and self.getSmellStrength() == "01":
            smellAuraSprite = arcade.Sprite("images/aura2_purple.png", scale)
        elif self.getSmellType() == "10" and self.getSmellStrength() == "10":
            smellAuraSprite = arcade.Sprite("images/aura3_purple.png", scale)
        elif self.getSmellType() == "10" and self.getSmellStrength() == "11":
            smellAuraSprite = arcade.Sprite("images/aura4_purple.png", scale)

        elif self.getSmellType() == "11" and self.getSmellStrength() == "01":
            smellAuraSprite = arcade.Sprite("images/aura2_blue.png", scale)
        elif self.getSmellType() == "11" and self.getSmellStrength() == "10":
            smellAuraSprite = arcade.Sprite("images/aura3_blue.png", scale)
        elif self.getSmellType() == "11" and self.getSmellStrength() == "11":
            smellAuraSprite = arcade.Sprite("images/aura4_blue.png", scale)

        if smellAuraSprite != 0:
            smellAuraSprite.center_x = self.coords[0]
            smellAuraSprite.center_y = self.coords[1]
            self.spriteList.append(smellAuraSprite)
        
        # handle cat fear
        catFearSprite = 0
        if self.getCatFear() == "00":
            catFearSprite = arcade.Sprite("images/catFear1.png", scale)
        elif self.getCatFear() == "01":
            catFearSprite = arcade.Sprite("images/catFear2.png", scale)
        elif self.getCatFear() == "10":
            catFearSprite = arcade.Sprite("images/catFear3.png", scale)
        elif self.getCatFear() == "11":
            catFearSprite = arcade.Sprite("images/catFear4.png", scale)
        catFearSprite.center_x = self.coords[0]
        catFearSprite.center_y = self.coords[1]
        self.spriteList.append(catFearSprite)

        # handle preference for metabolic rate
        metabolism = 0

        if self.getMetabolicRate() == "00":
            metabolism = arcade.Sprite("images/meta1.png", scale)
        elif self.getMetabolicRate() == "01":
            metabolism = arcade.Sprite("images/meta2.png", scale)
        elif self.getMetabolicRate() == "10":
            metabolism = arcade.Sprite("images/meta3.png", scale)
        elif self.getMetabolicRate() == "11":
            metabolism = arcade.Sprite("images/meta4.png", scale)
        metabolism.center_x = self.coords[0]
        metabolism.center_y = self.coords[1]
        self.spriteList.append(metabolism)

        mouseSprite = arcade.Sprite("images/mouse.png", scale)
        mouseSprite.center_x = self.coords[0]
        mouseSprite.center_y = self.coords[1]
        self.spriteList.append(mouseSprite)

        self.spriteList.draw()
        
        
        
        
        
        #arcade.draw_circle_filled(self.coords[0], self.coords[1], float(int(W/100)), arcade.color.LIGHT_BROWN)  

        

        

    