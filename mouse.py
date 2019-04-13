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

    def __init__(self, data):
        self.age = 0
        self.time = 0
        cheeseRoom = [random.randrange(W/10, W/5), random.randrange(0, H)]
        waterRoom = [random.randrange(W-(W/5), W-(W/10)), random.randrange(0, H)]
        self.coords = random.choice([cheeseRoom, waterRoom])
        self.spriteList = arcade.SpriteList()
        self.birthTime = time.clock()
        self.wanderDestination = [[-1, -1], 'x']
        self.takePassage = False
        self.mateCount = 0
        self.prepareToMate = False

        # 1 = eat, 2 = drink, 3 = reproduce, 4 = flee, 5 = wander, 6 = passage
        self.needState = random.choice([1,2])
        self.previousNeedState = -1

        self.stateClock = time.clock()

        #self.chromosome = strength + smellType + speed + metabolicRate + size + smallSpacePrefLevel + catFear
        self.chromosome = random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS) + random.choice(TRAITS)

        
        data.write(self.chromosome + "\n")
        

    def getMateCount(self):
        return self.mateCount

    def mateCountPlusPlus(self):
        self.mateCount = self.mateCount + 1

    def getBirthTime(self):
        return self.birthTime

    def getStateClock(self):
        return self.stateClock

    def setStateClock(self, time):
        self.stateClock = time 

    def getWanderDestination(self):
        return self.wanderDestination

    def setWanderDestination(self, coords, destination):
        self.wanderDestination[0] = coords
        self.wanderDestination[1] = destination
    def setNeedState(self, state):
        self.needState = state

    def setTakePassage(self, tOrF):
        self.takePassage = tOrF

    def getTakePassage(self):
        return self.takePassage

    def getNeedState(self):
        return self.needState

    def getCoords(self):
        return self.coords

    def setCoords(self, coords):
        self.coords = coords
        for sprite in self.spriteList:
            sprite.center_x = coords[0]
            sprite.center_y = coords[1]

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
        for x in range (0, len(self.spriteList)):
            self.spriteList.pop()
        
        
        
        
        
        #arcade.draw_circle_filled(self.coords[0], self.coords[1], float(int(W/100)), arcade.color.LIGHT_BROWN)  

        

        

    