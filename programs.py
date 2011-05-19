from collections import OrderedDict
from enum import Enum
from types import *
from pygame.locals import *
import config, random, pygame

dirs = Enum('UP', 'DOWN', 'LEFT', 'RIGHT')

class base(object):
    def __init__(self, name, sector, maxSize, speed, commands, color):
        self.name = name # Unfortunately, __name__ isn't kept after execution, so we need this.
        self.sectors = sector # All sectors that the program occupies in the form of [(x1,y1),(x2,y2),...(xn,yn)], initially None until used.
        self.maxSize = maxSize # The maximum size of the program in nodes.
        self.moves = 0
        self.speed = speed # How many squares it will be able to move at one time.
        self.commands = commands # A dictionary in the form of {Name: (Range, Strength, Description)} where range is how many squares
                                 # away it can attack, strength is how many nodes it can destroy, and description is its description.
        self.commands['No Action'] = (0, 0, 'Do nothing') # Add the standard 'No Action' command to pass the program's turn.
        self.color = color # Give the name of the color, right now no images since there isn't enough time.
        self.fired = False # Tells whether the program has fired (attacked) or not
        self.target = None # This is only used with autoMove, and just saves the target until the end of the turn to ease calculations.

    def move(self, direction):
        if (config.game.state == config.game.states.MapPlayer or config.game.state == config.game.states.MapEnemy) and self.moves < self.speed:
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
                if not config.player.squareTaken(x, y):
                    try: config.map.layout[y][x]
                    except IndexError: return False
                    else:
                        if config.map.layout[y][x] != 0:
                            self.sectors.insert(0, (x, y))
                            if not len(self.sectors) <= self.maxSize:
                                while len(self.sectors) > self.maxSize:
                                    del(self.sectors[-1])
                        else: return False
                    self.moves += 1
                elif config.game.state == config.game.states.MapEnemy:
                    done = True
                    for program in config.player.enemies:
                        if program.moves != program.speed:
                            adjacent = ((program.sectors[0][0]-1, program.sectors[0][1]), (program.sectors[0][0], program.sectors[0][1]-1), (program.sectors[0][0]+1, program.sectors[0][1]), (program.sectors[0][0], program.sectors[0][1]+1))
                            for x, y in adjacent:
                                if x>=0 and y>=0 and not config.player.squareTaken(x, y):
                                    done = False
                                    break
                            if not done: break
            else: return False
            if config.game.state == config.game.states.MapPlayer:
                config.map.programBorder['position'] = (self.sectors[0][0], self.sectors[0][1])
                if self.moves == self.speed:
                #    config.map.programBorder['selected'] = False
                #    config.map.programBorder['visible'] = False
                #    config.map.programBorder['position'] = None
                    config.player.checkIfDone()
            return True

    def autoMove(self):
        if self.target == None:
            closestProg = None
            for p in range(0, len(config.player.active)):
                program = config.player.active[p]
                d = [program.sectors[0][0]-self.sectors[0][0], program.sectors[0][1]-self.sectors[0][1]]
                sum = d[0] + d[1] if d[0] > 0 and d[1] > 0 else d[1]-d[0] if d[0] < 0 and d[1] > 0 else d[0]-d[1] if d[0] > 0 and d[1] < 0 else (d[0]+d[1])*-1
                d.append(sum)
                for sector in program.sectors:
                    dist = [sector[0]-self.sectors[0][0], sector[1]-self.sectors[0][1]]
                    sum = dist[0] + dist[1] if dist[0] > 0 and dist[1] > 0 else dist[1]-dist[0] if dist[0] < 0 and dist[1] > 0 else dist[0]-dist[1] if dist[0] > 0 and dist[1] < 0 else (dist[0]+dist[1])*-1
                    dist.append(sum)
                    if d[2] > dist[2]:
                        d = dist
                if closestProg == None:
                    closestProg = [program, d[0], d[1], d[2], p]
                elif closestProg[3] > d[2] or (closestProg[3] == d[2] and len(closestProg[0].sectors) > len(program.sectors)):
                        closestProg = [program, d[0], d[1], d[2], p]
            self.target = closestProg
        moved = False
        if (self.target[1] == 0 and (self.target[2] == 1 or self.target[2] == -1)) or (self.target[2] == 0 and (self.target[1] == 1 or self.target[1] == -1)):
            self.moves = self.speed
            self.target = None
        elif self.target[1] == 0 and self.target[2] > 1:
            moved = self.move(dirs.UP)
            self.target[2] += 1
        elif self.target[1] == 0 and self.target[2] < -1:
            moved = self.move(dirs.DOWN)
            self.target[2] -= 1
        elif self.target[2] == 0 and self.target[1] > 1:
            moved = self.move(dirs.LEFT)
            self.target[1] += 1
        elif self.target[2] == 0 and self.target[1] < -1:
            moved = self.move(dirs.RIGHT)
            self.target[1] -= 1
        else:
            dir = [dirs.UP, dirs.LEFT]
            if self.target[1] > 1:
                dir[1] = dirs.RIGHT
            if self.target[2] > 1:
                dir[0] = dirs.DOWN
            dir = dir[random.randint(0, 1)]
            moved = self.move(dir)
            if dir == dirs.UP and moved:
                self.target[2] += 1
            elif dir == dirs.DOWN and moved:
                self.target[2] -= 1
            elif dir == dirs.LEFT and moved:
                self.target[1] += 1
            elif dir == dirs.RIGHT and moved:
                self.target[1] -= 1
        return moved

class Hack(base):
    def __init__(self, sector=None):
        super(Hack, self).__init__('Hack', sector, 4, 2, OrderedDict([('Slice', (1, 2, 'Deletes 2 sectors\nfrom target'))]), 'red')

class Slingshot(base):
    def __init__(self, sector=None):
        super(Slingshot, self).__init__('Slingshot', sector, 2, 2, OrderedDict([('Fling', (3, 1, 'Deletes 1 sector\nfrom target'))]), 'green')

class Spammer(base):
    def __init__(self, sector=None, id=0):
        if type(sector) != (ListType, NoneType): sector = [sector]
        super(Spammer, self).__init__('Spammer', sector, 3, 1, OrderedDict([('Inject', (1, 3, 'Deletes three sectors\nfrom target.'))]), 'blue')
        self.id = id

# A renamed Hack, since Lego might not like me stealing their program names ;)
class Exploit(base):
    def __init__(self, sector=None):
        super(Exploit, self).__init__('Exploit', sector, 4, 2, OrderedDict([('Meddle', (1, 2, "Deletes 2 sectors\n from target"))]), 'red')

# And a renamed slingshot for the exact same reasons
class Browser(base):
    def __init__(self, sector=None):
        super(Browser, self).__init__('Browser', sector, 2, 2, OrderedDict([('Fling', (3, 1, 'Deletes 1 sector\nfrom target'))]), 'green')
