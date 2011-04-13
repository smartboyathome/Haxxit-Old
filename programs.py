from collections import OrderedDict
from enum import Enum
from types import *

dirs = Enum('UP', 'DOWN', 'LEFT', 'RIGHT')

class base(object):
    def __init__(self, name, sector, maxSize, speed, commands, color, ai):
        self.name = name # Unfortunately, __name__ isn't kept after execution, so we need this.
        self.sectors = sector # All sectors that the program occupies in the form of [(x1,y1),(x2,y2),...(xn,yn)], initially None until used.
        self.maxSize = maxSize # The maximum size of the program in nodes.
        self.moves = 0
        self.speed = speed # How many squares it will be able to move at one time.
        self.commands = commands # A dictionary in the form of {Name: (Range, Strength, Description)} where range is how many squares
                                 # away it can attack, strength is how many nodes it can destroy, and description is its description.
        self.commands['No Action'] = (0, 0, 'Do nothing') # Add the standard 'No Action' command to pass the program's turn.
        self.color = color # Give the name of the color, right now no images since there isn't enough time.
        self.ai = ai # Determines whether to use AI for this program.

    def move(self, player, map, game, direction):
        if game.started and self.moves < self.speed:
            if direction == dirs.DOWN:
                x = self.sectors[0][0]
                y = self.sectors[0][1]+1
            elif direction == dirs.UP:
                x = self.sectors[0][0]
                y = self.sectors[0][1]-1
            elif direction == dirs.LEFT:
                x = self.sectors[0][0]-1
                y = self.sectors[0][1]
            elif direction == dirs.RIGHT:
                x = self.sectors[0][0]+1
                y = self.sectors[0][1]
            if y >= 0 and x >= 0:
                squareTaken = False
                for program in player.programs: 
                    for xCoord, yCoord in self.sectors:
                        print "X: " + str(x) + " vs " + str(xCoord), "Y: " + str(y) + " vs " + str(yCoord)
                        if x == xCoord and y == yCoord:
                            squareTaken = True
                            break
                if not squareTaken:
                    try: map.layout[y][x]
                    except IndexError: pass
                    else:
                        if map.layout[y][x] != 0:
                            self.sectors.insert(0, (x, y))
                            if not len(self.sectors) <= self.maxSize:
                                while len(self.sectors) > self.maxSize:
                                    del(self.sectors[-1])
            self.moves += 1
            map.programBorder['position'] = (self.sectors[0][0], self.sectors[0][1])
            if self.moves == self.speed:
                map.programBorder['selected'] = False
                map.programBorder['visible'] = False
                map.programBorder['position'] = None

class Hack(base):
    def __init__(self, sector=None, ai=False):
        super(Hack, self).__init__('Hack', sector, 4, 2, OrderedDict([('Slice', (1, 2, 'Deletes two sectors\nfrom target'))]), 'red', ai)

class Slingshot(base):
    def __init__(self, sector=None, ai=False):
        super(Slingshot, self).__init__('Slingshot', sector, 2, 1, OrderedDict([('Fling', (3, 1, 'Deletes one sector\nfrom target'))]), 'green', ai)

class Spammer(base):
    def __init__(self, sector=None, ai=False):
        if type(sector) != (ListType, NoneType): sector = [sector]
        super(Spammer, self).__init__('Spammer', sector, 3, 1, OrderedDict([('Inject', (1, 3, 'Deletes three sectors\nfrom target.'))]), 'blue', ai)
