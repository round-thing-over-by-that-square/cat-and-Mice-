#Alex Lewandowski
#Cat and Mice
#Population class

import random
from mouse import Mouse

POP_SIZE = 50

class Population:
    def __init__(self):
        self.mice = []

    def getMice(self):
        return self.mice

    # Create an initial population of mice w random genotypes
    def generate(self):
        for i in range (0, POP_SIZE):
            self.mice.append(Mouse())
    
    # Reproduce and add offspring to self.mice
    def reproduce(self, mouse1Index, mouse2Index, crossoverPt):
        childChrom1 = ""
        childChrom2 = ""
        for i in range (0, crossoverPt):
            childChrom1 = childChrom1 + self.mice[mouse1Index].getChromosome()[i]
            childChrom2 = childChrom2 + self.mice[mouse2Index].getChromosome()[i]
        for x in range(crossoverPt, len(self.mice[mouse1Index].getChromosome())):
            childChrom1 = childChrom1 + self.mice[mouse2Index].getChromosome()[x]
            childChrom2 = childChrom2 + self.mice[mouse1Index].getChromosome()[x]
        childChrom1 = self.mutate(childChrom1)
        childChrom2 = self.mutate(childChrom2)
        child1 = Mouse()
        child2 = Mouse()
        child1.setCoords(self.mice[mouse1Index].getCoords())
        child2.setCoords(self.mice[mouse1Index].getCoords())
        child1.setChromosome(childChrom1)
        child2.setChromosome(childChrom2)
        self.mice.append(child1)
        self.mice.append(child2)

    def mutate(self, chromosome):
        x = random.randrange(0, 13)
        temp = ""
        for i in range (0, x):
            temp = temp + chromosome[i]
        if int(chromosome[x]) == 0:
                temp = temp + "1"
        else:
            temp = temp + "0"
        for i in range(x+1, len(chromosome)):
            temp = temp + chromosome[i]
        return chromosome

    def getIndex(self, mouse):
        for i in range (0, len(self.mice)):
            if self.mice[i] == mouse:
                return i
        return 0



