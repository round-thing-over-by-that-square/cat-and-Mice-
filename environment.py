#Alex Lewandowski
#Cat and Mice
#Environment Class

import arcade
import time
import math
import random
from random import uniform
from obstacle import Obstacle
from population import Population
from cat import Cat
from mouse import Mouse
from board import W
from board import H
from needs import Need
import copy
from population import DEATH_AGE
#DEATH_AGE = 200

class Environment(arcade.Sprite):
    def __init__(self):
        self.survivor = open("survivorData.txt", "a+")
        self.population = Population()
        self.population.generate()
        self.cat = Cat()
        objSprite1 = arcade.Sprite("images/obstacle_orange.png", 0.7)
        objSprite2 = arcade.Sprite("images/obstacle_teal.png", 0.5)
        self.obstacles = [Obstacle(objSprite1, [float(int(W-(W/3))), float(int(H - H/4))], H/9.25), Obstacle(objSprite2, [float(int(W/3)), float(int(H/25))], H/12)]
        self.allSafeZones = 0
        cheeseSprite = arcade.Sprite("images/cheese.png", 1)
        waterSprite = arcade.Sprite("images/water.png", 1)
        self.cheeseList = arcade.SpriteList()  
        self.waterList = arcade.SpriteList()     
        self.cheeseBasket = [Need('E', [W/20, H/5], copy.deepcopy(cheeseSprite)), Need('E', [W/20, 2*H/5], copy.deepcopy(cheeseSprite)), Need('E', [W/20, 3*H/5], copy.deepcopy(cheeseSprite)), Need('E', [W/20, 4*H/5], copy.deepcopy(cheeseSprite))]
        self.waterPitcher = [Need('D', [W-(W/20), H/5], copy.deepcopy(waterSprite)), Need('D', [W-(W/20), 2*H/5], copy.deepcopy(waterSprite)), Need('D', [W-(W/20), 3*H/5], copy.deepcopy(waterSprite)), Need('D', [W-(W/20), 4*H/5], copy.deepcopy(waterSprite))]
        for cheese in self.cheeseBasket:
            self.cheeseList.append(cheese.getSprite())
        for waterBowl in self.waterPitcher:
            self.waterList.append(waterBowl.getSprite())
    
    def draw(self):
        for obstacle in self.obstacles:
            obstacle.draw()
        self.waterList.draw()
        self.cheeseList.draw()
        for mouse in self.population.getMice():
            self.mouseMove(mouse) 
            mouse.draw()
        self.catMove()
        self.cat.draw()

    def getObstacles(self):
        return self.obstacles

    def getCat(self):
        return self.cat

    #Apply smell type and strength gene heuristics
    def adjustDistForSmell(self, distance, mouse):
        smellType = mouse.getSmellType()
        smellStrength = mouse.getSmellStrength()
        test1 = int(smellType, 2)
        test2 = int(smellStrength, 2)
        distance = distance - ((distance * int(smellType, 2)) / 25)
        return distance - ((distance * int(smellStrength, 2)) / 15)


    def distance(self, object1Coords, object2Coords):
        a = abs(object1Coords[0]-object2Coords[0])
        b = abs(object1Coords[1]-object2Coords[1])
        return math.sqrt(a*a + b*b)
        
 #   def move(self, coord, mouseOrCat, speed):
 #       #prevent divide by zero
 #       deltaX = (coord[0]-mouseOrCat.getCoords()[0])
 #       if deltaX == 0:
 #           deltaX = 99999999
 #       d = 1 * speed
 #       if self.distance(mouseOrCat.getCoords(), coord) <= d:
 #           #move to need coords
 #           mouseOrCat.setCoords([coord[0], coord[1]])
 #       midCoord = [coord[0], coord[1]]
 #       while self.distance(midCoord, mouseOrCat.getCoords()) >= d + 1.5:
 #           x = (mouseOrCat.getCoords()[0] + midCoord[0]) / 2
 #           y = (mouseOrCat.getCoords()[1] + midCoord[1]) / 2
 #           midCoord = [x, y]
 #       mouseOrCat.setCoords(midCoord)
        


    #moves mouse or cat towards current need by a distance related to it s speed 
    def move(self, coord, mouseOrCat, speed):

        #prevent divide by zero
        deltaX = (coord[0]-mouseOrCat.getCoords()[0])
        if deltaX == 0:
            deltaX = 99999999
        d = 1 * speed

        if self.distance(mouseOrCat.getCoords(), coord) <= d:
            #move to need coords
            mouseOrCat.setCoords([coord[0], coord[1]])
        midCoord = [coord[0], coord[1]]
        while self.distance(midCoord, mouseOrCat.getCoords()) >= d + 1.5:
            x = (mouseOrCat.getCoords()[0] + midCoord[0]) / 2
            y = (mouseOrCat.getCoords()[1] + midCoord[1]) / 2
            midCoord = [x, y]
        obstacle = self.isInObstacle(midCoord, type(mouseOrCat))
        if type(obstacle) == Obstacle:
            mouseOrCat.setCoords(midCoord)
            
            #mouseOrCat.setCoords(self.getAvoidObstacleCoords(mouseOrCat, obstacle))
        else:
            mouseOrCat.setCoords(midCoord)
        

    def findNearestCheeseDoor(self, mouse):
        cheeseDoors = [[W/5, H-(H/40)], [W/5, (H/2) - (H/40)], [W/5, (H/10) - (H/20)]]
        targetDoor = [[-1,-1], 1000000]
        for door in cheeseDoors:
            dist = self.distance(mouse.getCoords(), door)
            if  dist < targetDoor[1]:
                targetDoor[0] = door
                targetDoor[1] = dist
        return targetDoor[0]

    def findNearestCheese(self, mouse):
        targetCheese = [[-1,-1], 100000]
        for cheese in self.cheeseBasket:
            dist = self.distance(cheese.getCoords(), mouse.getCoords())
            if dist < targetCheese[1]:
                targetCheese = [cheese, dist]
        return targetCheese[0].getCoords()

    def findNearestWater(self, mouse):
        targetWaterDish = [[-1, -1], 100000]
        for waterDish in self.waterPitcher:
            dist = self.distance(waterDish.getCoords(), mouse.getCoords())
            if dist < targetWaterDish[1]:
                targetWaterDish = [waterDish, dist]
        return targetWaterDish[0].getCoords()

    def findNearestWaterDoor(self, mouse):
        waterDoors = [[W - (W/5), H-(H/20)], [W - (W/5), (H/2)-(H/40)]]
        targetDoor = [[-1, -1], 1000000]
        for door in waterDoors:
            dist = self.distance(mouse.getCoords(), door)
            if  dist < targetDoor[1]:
                targetDoor[0] = door
                targetDoor[1] = dist
        return targetDoor[0]

    def isInsideWaterRoom(self, mouse):
        if mouse.getCoords()[0] > W - (W/5):
            return True
        else:
            return False

    def isInsideCheeseRoom(self, mouse):
        if mouse.getCoords()[0] < W/5:
            return True
        else:
            return False

    def isInsideCatRoom(self, mouseOrCat):
        if mouseOrCat.getCoords()[1] > H/20 and mouseOrCat.getCoords()[0] > W/5 and ((mouseOrCat.getCoords()[0] < float(int(W - (W/5) - (H/30))) and  mouseOrCat.getCoords()[1] <= float(int(H - (H/2) - (H/20)))) or (mouseOrCat.getCoords()[0] < (float(int(W - (W/5)))) and mouseOrCat.getCoords()[1] >= float(int(H - (H/2) - (H/20))))):
            return True
        else:
            return False
    

    

    def ponderPassage(self, mouse):
        if self.isInsideWaterRoom(mouse) or self.isInsideCheeseRoom(mouse):
            # smallest mouse: never take
            if mouse.getSmallSpacePrefLevel() == "00" and mouse.getSize() == "00":
                mouse.setTakePassage(False)
            # smallest mouse: take 25% of time
            elif mouse.getSmallSpacePrefLevel() == "01" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, False, False, False]))
            # smallest mouse: take 50% of time
            elif mouse.getSmallSpacePrefLevel() == "10" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, False]))
            # smallest mouse: take 75% of time
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "00":
                mouse.setTakePassage(random.choice([True, True, True, False]))
            
            # second-smallest mouse: never take
            elif mouse.getSmallSpacePrefLevel() == "01" and mouse.getSize() == "01":
                mouse.setTakePassage(False)
            # second-smallest mouse: take 16.6% of the time
            elif mouse.getSmallSpacePrefLevel() == "10" and mouse.getSize() == "01":
                mouse.setTakePassage(random.choice([True, False, False, False, False, False]))
            # second-smallest mouse: take 25% of the time
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "01":
                mouse.setTakePassage(random.choice([True, False, False, False]))
            # second-smallest mouse: take 40% of the time
            elif mouse.getSmallSpacePrefLevel() == "11" and mouse.getSize() == "01":
                mouse.setTakePassage(random.choice([True, True, False, False, False,]))
            else:
                mouse.setTakePassage(False)
        else:
            mouse.setTakePassage(False)


    def wander(self, mouse, speed):
        if (self.isInsideCheeseRoom(mouse) and mouse.getWanderDestination()[0] == [-1, -1]):# or self.distance(mouse.getWanderDestination(), mouse.getCoords()) < H/80:
            destination = [uniform(W/10, (W/5)-(H/80)), uniform(0, H)]
            mouse.setWanderDestination(destination, 'x')
            self.move(destination, mouse, speed)
        elif (self.isInsideWaterRoom(mouse) and mouse.getWanderDestination()[0] == [-1, -1]):# or self.distance(mouse.getWanderDestination(), mouse.getCoords()) < H/80:
            destination1 = [uniform(W-W/10, W-W/5+(H/80)), uniform(0, H)]
            mouse.setWanderDestination(destination1, 'x')
            self.move(destination1, mouse, speed)
        elif mouse.getWanderDestination()[0] != [-1, -1]:
            if self.distance(mouse.getWanderDestination()[0], mouse.getCoords()) > H/80:
                self.move(mouse.getWanderDestination()[0], mouse, speed)
            else:
                mouse.setWanderDestination([-1, -1], 'x')

     #Cat move utility function
    def targetMouse(self): #still needs to factor in smell type and strength and ignore out of sight mice
        target = [self.population.getMice()[0], 10000000]
        for mouse in self.population.getMice():
            distance = self.distance(self.cat.getCoords(), mouse.getCoords())
            distance = self.adjustDistForSmell(distance, mouse)
            for obstacle in self.obstacles:
                if self.isBetween(mouse.getCoords(), self.cat.getCoords(), obstacle):
                    if  distance < target[1] and self.isInsideCatRoom(mouse):
                        target[0] = mouse
                        target[1] = distance
                        break
        if target[1] != 10000000:
            return target[0]
        else:
            return 0

    def catMove(self):
        target = self.cat.getTarget()
        if type(target) == int or not self.isInsideCatRoom(target):
            target = self.targetMouse()
            self.cat.setTarget(target)
        if type(target) != int:
            self.move(target.getCoords(), self.cat, 13)

            if self.distance(self.cat.getCoords(), target.getCoords()) < H/10:
                self.cat.setTarget(0)
        else:
            #self.cat.setWanderDestination([-1, -1], 'x')
            self.catWander()

    def catWander(self):
        if self.cat.getWanderDestination()[0] == [-1, -1]:
            destination1 = [uniform(W/5, W-W/5+(H/80)), uniform(H/15, H)]
            self.cat.setWanderDestination(destination1, 'x')
            self.move(destination1, self.cat, 1)
        else:
            if self.distance(self.cat.getWanderDestination()[0], self.cat.getCoords()) > H/80:
                self.move(self.cat.getWanderDestination()[0], self.cat, 4)
            else:
                self.cat.setWanderDestination([-1, -1], 'x')

    

    #################################################################################################
    ## Obstacle and Hidden Zone Utility Functions
    #################################################################################################

    def isInObstacle(self, coords, type):
        for obstacle in self.obstacles:
            if type == Cat:
                if self.distance(obstacle.getCoords(), coords) < obstacle.getRadius() + H/15:
                    return obstacle
            elif type == Mouse:
                if self.distance(obstacle.getCoords(), coords) < obstacle.getRadius() + H/40:
                    return obstacle
            else:
                return 0

    def getAvoidObstacleCoords(self, object, obstacle):
        if object.getCoords()[0] - obstacle.getCoords()[0] == 0:
            m = 999999
        else:
            m = (object.getCoords()[1] - obstacle.getCoords()[1]) / (object.getCoords()[0] - obstacle.getCoords()[0])
        x = object.getCoords()[0]
        y = object.getCoords()[1]
        b = object.getCoords()[1] - (m * x)
        
        m = -1 / m
        if m <= 0.5 and m <= 1.5:
            x = x + (obstacle.getRadius() * 0.6)
            y = m * x + b
        elif m > 1.5:
            y = y + obstacle.getRadius()
            x = (y - b) / m
        elif m < 0.5 and m >= 0:
            x = x + obstacle.getRadius()
            y = m * x + b
        elif m < 0 and m >= -0.5:
            x = x + (obstacle.getRadius() * 0.6)
            y = m * x + b
        elif m < -0.5 and m >= -1.5:
            y = y - obstacle.getRadius()
            x = (y - b) / m
        elif m < 1.5:
            x = x + obstacle.getRadius()
            y = m * x + b

        return [x,y]
    


     #is the object between the two coordinated
    def isBetween(self, coords1, coords2, object):
        verticies = []
        if ((coords1[0] - coords2[0])) == 0:
            m = 999999
        else:
            m = (coords1[1] - coords2[1])/(coords1[0] - coords2[0])
        x = coords2[0]
        y = coords2[1]
        b = coords2[1] - (m * x)

        #Handle undefined slopes
        vertY = int(coords2[1])
        if coords1[1] > coords2[1] and m == .00000001:
            for i in range (0, int(coords2[1])):
                if i%10 == 0:
                    vertY = vertY - 10
                    if vertY > H/40 and vertY < H and x < W - (W/5) - (H/40) and x > W/5:
                        verticies.append([x,vertY])
        elif coords1[1] < coords2[1] and m == .00000001:
            for i in range (0, int(H - coords2[1])):
                if i%10 == 0:
                    vertY = vertY + 10
                    if vertY > H/40 and vertY < H and x < W - (W/5) - (H/40) and x > W/5:
                        verticies.append([x,vertY])

        #Handle defined slopes
        else:
            for i in range (0, 100):
                y = ((m * x) + b) 
                if y > H/20 and y < H and x < W - (W/5) - (H/20) and x > W/5:
                    verticies.append([x,y])
                if coords1[1] > coords2[1]:
                    if m < 0:
                        x = x + 10
                    else:
                        x = x - 10
                else:
                    if m > 0:
                        x = x + 10
                    else:
                        x = x - 10
        for vertexCoords in verticies:
            if self.distance(vertexCoords, self.cat.getCoords()) < object.getRadius():
                return True
        return False

        
            
    ################################################################################################################################
    ################################################################################################################################
    # Heuristics that factor into move direction:
    # -needState: 1-3 go towards, 4 go away from
    # -preferenceForConfinedSpaces, increased probablility of taking confined route, if small enough to fit
    # -make short runs to safe zones
    # -when fleeing, only run to real safe zones
    # -if obstacle in the way of real safe zone, recaluclate to the route around it to closest real path  
    def mouseMove(self, mouse):

        #Apply speed gene gene  
        if mouse.getSpeed() == "00":
            speed = 5 #1 #.5
        if mouse.getSpeed() == "01":
            speed = 10 #2 #1
        if mouse.getSpeed() == "10":
            speed = 15 #4 #2
        if mouse.getSpeed() == "11":
            speed = 20 #8 #5

        #Apply metabolic rate gene
        if mouse.getMetabolicRate() == "00":
            metabolicRate = 1
        if mouse.getMetabolicRate() == "01":
            metabolicRate = 1.3
        if mouse.getMetabolicRate() == "10":
            metabolicRate = 1.6
        if mouse.getMetabolicRate() == "11":
            metabolicRate = 2


        #Apply catFear gene
        if mouse.getCatFear() == "00":
            fearDistance = H/10
        if mouse.getCatFear() == "01":
            fearDistance = H/7
        if mouse.getCatFear() == "10":
            fearDistance = H/5
        if mouse.getCatFear() == "11":
            fearDistance = H/3

        # Mouse dies of old age
        if time.clock() - mouse.getBirthTime() > DEATH_AGE and mouse.getNeedState() != 3:
            c = mouse.getChromosome()
            self.survivor.write(c[0]+c[1]+","+ c[2]+c[3]+","+ c[4]+c[5]+","+ c[6]+c[7]+","+ c[8]+c[9]+","+ c[10]+c[11]+","+ c[12]+c[13]+"\n")
        
            self.population.killMouse(mouse)

        # Mouse gets eaten
        if self.distance(mouse.getCoords(), self.cat.getCoords()) < H/15:
              self.population.killMouse(mouse)

        #Trigger flee state if the cat is within mouse's fear distance
        if self.distance(mouse.getCoords(), self.cat.getCoords()) < fearDistance:
            if mouse.getCoords()[0] > W/5 and mouse.getCoords()[1] > H/20 and mouse.getCoords()[0] < W-(W/5)-(H/39):
                mouse.setNeedState(4)
            elif mouse.getCoords()[0] > W-(W/5)-(H/30) and mouse.getCoords()[1] > (H/2) + (H/40) and mouse.getCoords()[0] < W-(W/5):
                mouse.setNeedState(4)

        

        #if need state = Eat   
        if mouse.getNeedState() == 1:
            goNorth = [mouse.getCoords()[0], (H/3)]
            if time.clock() - mouse.getStateClock() > 35:
                self.population.killMouse(mouse) #dies of starvation
            cheeseDoorCoord = self.findNearestCheeseDoor(mouse)
            waterDoorCoord = self.findNearestWaterDoor(mouse)
            if not self.isInsideCheeseRoom(mouse):
                if mouse.getTakePassage() == -1:
                    #ponder taking the passage (if mouse is small enough)
                    self.ponderPassage(mouse)
                if self.isInsideWaterRoom(mouse) and mouse.getCoords()[1] < H/3:
                    mouse.setWanderDestination(goNorth, 'n')
                    self.move(mouse.getWanderDestination()[0], mouse, speed)
                elif self.isInsideWaterRoom(mouse) and mouse.getTakePassage() == True:
                    mouse.setNeedState(6)
                    #self.move([W-(W/5)-(H/40), (H/2)-(H/40)], mouse, speed)
                elif self.isInsideWaterRoom(mouse) and mouse.getTakePassage() == False:
                    self.move([waterDoorCoord[0] - (H/150), waterDoorCoord[1]], mouse, speed)##############
                else:
                    self.move([cheeseDoorCoord[0] -(H/80), cheeseDoorCoord[1]], mouse, speed)
            else: #inside cheeseroom
                cheeseCoord = self.findNearestCheese(mouse)
                if self.distance(mouse.getCoords(), cheeseCoord) > H/40:
                    mouse.setWanderDestination([-1, -1], 'x')
                    self.move(cheeseCoord, mouse, speed)
                else:
                    mouse.setStateClock(time.clock())
                    self.ponderPassage(mouse)
                    if mouse.getMateCount() < 3 and time.clock() - mouse.getBirthTime() > 5:
                        mouse.prepareToMate = True
                    mouse.setNeedState(5)


                

        #if need state = Drink
        elif mouse.getNeedState() == 2:
            if time.clock() - mouse.getStateClock() > 35: 
                self.population.killMouse(mouse) #dies of thirst 
            if not self.isInsideWaterRoom(mouse):
                if mouse.getTakePassage() == -1:
                    #ponder taking the passage (if mouse is small enough)
                    self.ponderPassage(mouse)
                cheeseDoorCoord = self.findNearestCheeseDoor(mouse)
                waterDoorCoord = self.findNearestWaterDoor(mouse)
                if self.isInsideCheeseRoom(mouse) and mouse.getTakePassage() == True:
                    mouse.setNeedState(6)
                elif self.isInsideCheeseRoom(mouse) and mouse.getTakePassage() == False:
                    self.move([cheeseDoorCoord[0] + (H/80), cheeseDoorCoord[1]], mouse, speed)
                else:
                    self.move([waterDoorCoord[0] + (H/80), waterDoorCoord[1]], mouse, speed)
            else:
                waterCoord = self.findNearestWater(mouse)
                if self.distance(mouse.getCoords(), waterCoord) > H/40:
                    mouse.setWanderDestination([-1, -1], 'x')
                    self.move(waterCoord, mouse, speed)
                else:
                    mouse.setStateClock(time.clock())
                    self.ponderPassage(mouse)
                    if mouse.getMateCount() < 3 and time.clock() - mouse.getBirthTime() > 5:
                        mouse.prepareToMate = True
                    mouse.setNeedState(5)

    

        #if need state = Reproduce    
        elif mouse.getNeedState() == 3:
            matePair = self.population.getMatingPair()
            if matePair == []: #then look for a mate
                potentialMate = [mouse, 10000000]
                for m in self.population.getMice():
                    d = self.distance(mouse.getCoords(), m.getCoords())
                    if d < potentialMate[1] and m != mouse and m.getNeedState() == 3:
                        if (self.isInsideCheeseRoom(m) and self.isInsideCheeseRoom(mouse)) or (self.isInsideWaterRoom(m) and self.isInsideWaterRoom(mouse)):
                            potentialMate[0] = m
                            potentialMate[1] = d
                if potentialMate[0] != mouse:
                    self.population.setMatingPair([mouse, potentialMate[0]])
                    mouse.setStateClock(time.clock())
                    potentialMate[0].setStateClock(time.clock())
                else: # wait for a mouse in your room to go into heat
                    self.wander(mouse, speed)
            if matePair != []:
                if matePair[0] == mouse:
                    mate = matePair[1]
                else:
                    mate = matePair[0]
                if self.distance(mouse.getCoords(), mate.getCoords()) < H/20:
                    self.population.reproduce(self.population.getIndex(mouse), self.population.getIndex(mate), random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13]))
                    mouse.mateCountPlusPlus()
                    mate.setStateClock(time.clock())
                    mate.setNeedState(1)
                    mouse.setStateClock(time.clock())
                    mouse.setNeedState(2)
                    self.population.setMatingPair([])
                        
                elif (time.clock() - matePair[0].getStateClock() < 10) and (time.clock() - matePair[1].getStateClock() < 10):
                    self.move(mate.getCoords(), mouse, speed)
                else:
                    # mouse could be either index in matePair
                    matePair[0].setStateClock(time.clock())
                    matePair[0].setNeedState(5)
                    matePair[1].setStateClock(time.clock())
                    matePair[1].setNeedState(5)
        
        #if need state = flee
        elif mouse.getNeedState() == 4:
            safeCoord = self.getFleeCoord(mouse)
            self.move(safeCoord, mouse, speed)
            if self.distance(mouse.getCoords(), safeCoord) < H/80:
                mouse.setStateClock(time.clock() + 25)
                mouse.setNeedState(5)

        #if need state = wander
        elif mouse.getNeedState() == 5:
            if time.clock() - mouse.getStateClock() > 30 * metabolicRate and mouse.prepareToMate == False: 
                if self.isInsideCheeseRoom(mouse):
                    mouse.setStateClock(time.clock())
                    mouse.setNeedState(2)
                else:
                    mouse.setStateClock(time.clock())
                    mouse.setNeedState(1)
            elif time.clock() - mouse.getStateClock() > 5 and mouse.prepareToMate == True:
                mouse.prepareToMate = False
                if len(self.population.mice) < 130: 
                    mouse.setNeedState(3)
                else:
                    mouse.setStateClock(time.clock() + 5.1)
                    mouse.setNeedState(5)
            else:
                self.wander(mouse, speed)

        #if taking passage
        elif mouse.getNeedState() == 6:
            coords = mouse.getCoords()
            passageEntranceWater = [W-(W/5)-(H/60), (H/2 - H/20)]
            passageEntranceCheese = [W/5, H/40]
            passageCorner = [W-(W/5)-(H/60), H/40]
            
            # if in water room
            if coords[0] > W-(W/5) and mouse.getWanderDestination()[1] != 'c' and mouse.getWanderDestination()[1] != 'w':
                mouse.setWanderDestination(passageEntranceWater, 'c')
            elif self.distance(coords, passageEntranceWater) < H/80 and mouse.getWanderDestination()[1] == 'c':
                mouse.setWanderDestination(passageCorner, 'c')
            elif self.distance(coords, passageCorner) < H/80 and mouse.getWanderDestination()[1] == 'c':
                mouse.setWanderDestination(passageEntranceCheese, 'c')
            elif self.distance(coords, passageEntranceCheese) < H/80 and mouse.getWanderDestination()[1] == 'c':
                mouse.setStateClock(time.clock())
                mouse.setNeedState(1)
            

            # if in cheese room
            elif coords[0] < (W/5) and mouse.getWanderDestination()[1] != 'c' and mouse.getWanderDestination()[1] != 'w':
                mouse.setWanderDestination(passageEntranceCheese, 'w')
            elif self.distance(coords, passageEntranceCheese) < H/80 and mouse.getWanderDestination()[1] == 'w':
                mouse.setWanderDestination(passageCorner, 'w')
            elif self.distance(coords, passageCorner) < H/80 and mouse.getWanderDestination()[1] == 'w':
                mouse.setWanderDestination(passageEntranceWater, 'w')
            elif self.distance(coords, passageEntranceWater) < H/80 and mouse.getWanderDestination()[1] == 'w':
                mouse.setStateClock(time.clock())
                mouse.setNeedState(2)

            self.move(mouse.getWanderDestination()[0], mouse, speed)


    ################################################################################################################################# #Mouse Move Utility Functions
    ###############################################################################################################################         
   
    def getFleeCoord(self, mouse):
        fleecoords = [[float(int(W/5)-(H/40)), float(int(H - H/40))], [float(int(W/5)-(H/40)), float(int(H - (H/2) - (H/40)))], [float(int((W - (W/5))+(H/40))), (float(int(H - H/40)))], [float(int(W - (W/5)+(H/40))), float(int(H - (H/2) - (H/40)))]]
        minDist = [0, 1000000]
        for coord in fleecoords:
            d = self.distance(mouse.getCoords(), coord)
            if d < minDist[1] and not self.isBetween(mouse.getCoords(), coord, self.cat):
                minDist[0] = coord
                minDist[1] = d
        return minDist[0]

    def setSafeZones(self, obstacles, cat):
        allSafeCoords = []
        for obstacle in obstacles:
            safeCoords = self.mapSafeZone(obstacle, cat)
            for coord in safeCoords:
                allSafeCoords.append(coord)
        self.allSafeZones = allSafeCoords

    def mapSafeZone(self, obstacle, cat):
        safeZone = []
        if ((cat.getCoords()[0] - obstacle.getCoords()[0])) == 0:
            m = .00000001
        else:
            m = (cat.getCoords()[1] - obstacle.getCoords()[1])/(cat.getCoords()[0] - obstacle.getCoords()[0])
        x = obstacle.getCoords()[0]
        y = obstacle.getCoords()[1]
        b = obstacle.getCoords()[1] - (m * x)

        #Handle undefined slopes
        if cat.getCoords()[1] > obstacle.getCoords()[1] and m == .00000001:
            vertY = int(obstacle.getCoords()[1] - obstacle.getRadius())
            for i in range (0, int(obstacle.getCoords()[1] - obstacle.getRadius())):
                if i%10 == 0:
                    vertY = vertY - 10
                    if vertY > H/40 and vertY < H and x < W - (W/5) - (H/40) and x > W/5:
                        safeZone.append([x,vertY])
        elif cat.getCoords()[1] < obstacle.getCoords()[1] and m == .00000001:
            vertY = int(obstacle.getCoords()[1] + obstacle.getRadius())
            for i in range (0, int(H - obstacle.getCoords()[1] + obstacle.getRadius())):
                if i%10 == 0:
                    vertY = vertY + 10
                    if vertY > H/40 and vertY < H and x < W - (W/5) - (H/40) and x > W/5:
                        safeZone.append([x,vertY])

        #Handle defined slopes
        else:
            for i in range (0, 100):
                y = ((m * x) + b) 
                if y > H/20 and y < H and x < W - (W/5) - (H/20) and x > W/5:
                    if self.getDistance([x,y], [obstacle.getCoords()[0], obstacle.getCoords()[1]]) > obstacle.getRadius():
                        safeZone.append([x,y])
                if cat.getCoords()[1] > obstacle.getCoords()[1]:
                    if m < 0:
                        x = x + 10
                    else:
                        x = x - 10
                else:
                    if m > 0:
                        x = x + 10
                    else:
                        x = x - 10
        return safeZone

    #return distance between two coords
    def getDistance(self, coord1, coord2):
        return math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)

    #(int(W/5), int(W - W/5)): #only search in the cat room
    def findNearestSafeZone(self, mouse):
        minCoord = [[-1, -1], 10000000]
        for coord in self.allSafeZones:
            d = self.distance(mouse.getCoords(), coord)
            if  d < minCoord[1]:
                minCoord = [coord, d]
        return minCoord[0]

    def takeTunnel(self, mouse):
        if mouse.getSize().self.getStringBin() == 0:
            takeTun = random.choice([True, True, False])
            return takeTun
        else:
            return False

    #distance at which mouse will allow cat to get before fleeing affected by catFear
    def flee(self, mouse, cat):
        return "dummy coord"

   