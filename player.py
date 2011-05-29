import copy, programs as progs, pygame, config, misc
from pygame.locals import *

class Programs():
    selection = False
    current = None
    active = []
    enemies = []
    programs = [('Hack', 2, 2), ('Slingshot', 2, 2)]
    
    def __init__(self, progs=None):
        if progs != None:
            programs += progs

    def gen(self):
        self.active = copy.deepcopy(config.map.spawns)
        id = 1
        for enemy in config.map.enemies:
            self.enemies.append(getattr(progs, enemy[0])(enemy[1],id))
            id += 1

    def squareTaken(self, x, y, playerOnly=False):
        try: config.map.layout[y][x]
        except IndexError: return True
        if config.map.layout[y][x] == 0: return True
        if playerOnly: Progs = self.active
        else: Progs = self.active + self.enemies
        for program in Progs: 
            for xCoord, yCoord in program.sectors:
                #print "X: " + str(x) + " vs " + str(xCoord), "Y: " + str(y) + " vs " + str(yCoord)
                if x == xCoord and y == yCoord:
                    return True
        return False

    def checkIfDone(self):
        done = True
        tmp = self.active if config.game.state.Map.turn.Player in config.game.states else self.enemies
        for program in tmp:
            if program.moves != program.speed:
                adjacent = ((program.sectors[0][0]-1, program.sectors[0][1]), (program.sectors[0][0], program.sectors[0][1]-1), (program.sectors[0][0]+1, program.sectors[0][1]), (program.sectors[0][0], program.sectors[0][1]+1))
                for x, y in adjacent:
                    if x>=0 and y>=0 and not self.squareTaken(x, y):
                        if config.game.state.Map.turn.Enemy in config.game.states:
                            moved = False
                            while not moved:
                                moved = program.autoMove()
                        done = False
                        break
                if config.game.state.Map.turn.Enemy in config.game.states and not done: break
        if done and config.game.state.Map.turn.Player in config.game.states:
            config.game.states.add(config.game.state.Map.turn.Enemy)
            for program in self.enemies:
                program.moves = 0
            pygame.time.set_timer(USEREVENT+1, 1500)
        elif done and config.game.state.Map.turn.Enemy in config.game.states:
            config.game.states.add(config.game.state.Map.turn.Player)
            for program in self.active:
                program.moves = 0
            pygame.time.set_timer(USEREVENT+1, 0)

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                config.game.states.add(config.game.state.Quit)
                break
            elif event.type == USEREVENT+1: # if doing the enemy event
                self.checkIfDone()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    config.game.states.add(config.game.state.Quit)
                    break
                elif event.key == K_UP:
                    if config.game.state.Map.turn.Player in config.game.states and config.map.programBorder['selected']:
                        self.active[config.map.programBorder['option']].move(progs.dirs.UP)
                elif event.key == K_DOWN:
                    if config.game.state.Map.turn.Player in config.game.states and config.map.programBorder['selected']:
                        self.active[config.map.programBorder['option']].move(progs.dirs.DOWN)
                elif event.key == K_LEFT:
                    if config.game.state.Map.turn.Player in config.game.states and config.map.programBorder['selected']:
                        self.active[config.map.programBorder['option']].move(progs.dirs.LEFT)
                elif event.key == K_RIGHT:
                    if config.game.state.Map.turn.Player in config.game.states and config.map.programBorder['selected']:
                        self.active[config.map.programBorder['option']].move(progs.dirs.RIGHT)
                else: print("Key not bound: " + event.key)
            elif event.type == MOUSEMOTION:
                x, y = event.pos
                if config.game.state.Map.turn.Init in config.game.states and not config.map.spawnBorder['selected']:
                    for xCoord, yCoord in config.map.spawns:
                        x1 = (xCoord+1)*35+150
                        y1 = (yCoord+1)*35+15
                        if (x-x1)**2 + (y-y1)**2 <= 5**2:
                            config.map.spawnBorder['visible'] = True
                            config.map.spawnBorder['position'] = (xCoord, yCoord)
                            break
                        else:
                            config.map.spawnBorder['visible'] = False
                            config.map.spawnBorder['position'] = None
                elif config.game.state.Map.turn.Player in config.game.states or config.game.state.Map.turn.Enemy in config.game.states:
                    if not config.map.programBorder['selected']:
                        for program in self.active:
                            x1 = (program.sectors[0][0]+1)*35+150
                            y1 = (program.sectors[0][1]+1)*35+15
                            if (x-x1)**2 + (y-y1)**2 <= 10**2:
                                config.map.programBorder['visible'] = True
                                config.map.programBorder['position'] = (program.sectors[0][0], program.sectors[0][1])
                                break
                            else:
                                config.map.programBorder['visible'] = False
                                config.map.programBorder['position'] = None
                if (15 < x and x < 145) and (15 < y and y < 150):
                    for num in range(1, len(self.programs)+1):
                        if num*12+18 < y and y < (num+1)*12+18:
                            config.draw.selectBox['visible'] = True
                            config.draw.selectBox['option'] = num
                            break
                        else:
                            config.draw.selectBox['visible'] = False
                            config.draw.selectBox['option'] = 0
                else:
                    config.draw.selectBox['visible'] = False
                    config.draw.selectBox['option'] = 0
                
                if (15 < x and x < 130) and (240 < y and y < 465) and config.draw.infoBox['visible']:
                    if type(config.draw.infoBox['program']) is tuple:
                        program = getattr(progs, config.draw.infoBox['program'][0])()
                    else:
                        program = config.draw.infoBox['program']
                    for num, name in zip(range(0, len(program.commands)), program.commands):
                        if num*10+243 < y and y < (num+1)*10+243:
                            config.draw.infoBox['comHover'] = num
                            break
                        else:
                            config.draw.infoBox['comHover'] = None
                else:
                    config.draw.infoBox['comHover'] = None

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if config.game.state.Map.turn.Init in config.game.states:
                    for xCoord, yCoord in config.map.spawns:
                        x1 = (xCoord+1)*35+150
                        y1 = (yCoord+1)*35+15
                        if (x-x1)**2 + (y-y1)**2 <= 5**2:
                            config.map.spawnBorder['selected'] = True
                            config.draw.selectBox['visible'] = False
                            config.draw.selectBox['option'] = 0
                            config.draw.infoBox['visible'] = False
                            config.draw.infoBox['program'] = None
                            config.draw.infoBox['comSelect'] = None
                            break
                        elif (15 < x and x < 155) and (15 < y and y < 150):
                            pass
                        else:
                            config.map.spawnBorder['selected'] = False
                            config.map.spawnBorder['visible'] = False
                    if (585 < x and x < 635) and (460 < y and y < 475):
                        if config.game.state.Map.turn.Init in config.game.states and not misc.anyEqual(self.active, config.map.spawns):
                            config.game.states.add(config.game.state.Map.turn.Player)
                elif config.game.state.Map.turn.Player in config.game.states or config.game.state.Map.turn.Enemy in config.game.states:
                    for num, program in zip(range(0, len(self.active)),self.active):
                        x1 = (program.sectors[0][0]+1)*35+150
                        y1 = (program.sectors[0][1]+1)*35+15
                        if (x-x1)**2 + (y-y1)**2 <= 10**2 and not self.active[num].fired:
                            config.map.programBorder['selected'] = True
                            config.map.programBorder['visible'] = True
                            config.map.programBorder['position'] = (program.sectors[0][0], program.sectors[0][1])
                            config.map.programBorder['option'] = num
                            config.draw.infoBox['visible'] = True
                            config.draw.infoBox['program'] = program
                            config.draw.attackDict['visible'] = False
                            config.draw.attackDict['program'] = None
                            config.draw.attackDict['command'] = None
                            config.draw.attackDict['squares'] = []
                            break
                        elif (15 < x and x < 155) and (175 < y and y < 465):
                            pass
                        else:
                            config.map.programBorder['selected'] = False
                            config.map.programBorder['visible'] = False
                            config.map.programBorder['position'] = None
                            config.draw.infoBox['visible'] = False
                            config.draw.infoBox['program'] = None
                            config.draw.attackDict['visible'] = False
                            config.draw.attackDict['program'] = None
                            config.draw.attackDict['command'] = None
                            config.draw.attackDict['squares'] = []
                if (15 < x and x < 155) and (15 < y and y < 150):
                    for num in range(1, len(self.programs)+1):
                        if (num*12+18 < y and y < (num+1)*12+18) and not config.draw.infoBox['program'] == self.programs[num-1]:
                            if not config.map.spawnBorder['selected']:
                                config.draw.infoBox['visible'] = True
                                config.draw.infoBox['program'] = self.programs[num-1]
                            elif self.programs[num-1][1] > 0:
                                try: self.active[config.map.spawns.index(config.map.spawnBorder['position'])].name
                                except AttributeError:
                                    self.programs[num-1] = (self.programs[num-1][0], self.programs[num-1][1] - 1, self.programs[num-1][2])
                                    self.active[config.map.spawns.index(config.map.spawnBorder['position'])] = getattr(progs, self.programs[num-1][0])([config.map.spawnBorder['position']])
                                else:
                                    if type(self.active[config.map.spawns.index(config.map.spawnBorder['position'])]) == type(getattr(progs, self.programs[num-1][0])([config.map.spawnBorder['position']])):
                                        for num in range(0, len(self.programs)):
                                            if self.programs[num][0] == self.active[config.map.spawns.index(config.map.spawnBorder['position'])].name:
                                                self.programs[num] = (self.programs[num][0], self.programs[num][1] + 1, self.programs[num][2])
                                        self.active[config.map.spawns.index(config.map.spawnBorder['position'])] = config.map.spawns[config.map.spawns.index(config.map.spawnBorder['position'])]
                                    else:
                                        pass
                                        # DOES NOT WORK
                                        #for num in range(0, len(self.programs)):
                                        #    if self.programs[num][0] == self.active[config.map.spawns.index(config.map.spawnBorder['position'])].name:
                                        #        self.programs[num] = (self.programs[num][0], self.programs[num][1] + 1, self.programs[num][2])
                                        #self.programs[num] = (self.programs[num][0], self.programs[num][1] - 1, self.programs[num][2])
                                        #self.active[config.map.spawns.index(config.map.spawnBorder['position'])] = getattr(progs, self.programs[num][0])([config.map.spawnBorder['position']])
                                config.map.spawnBorder['selected'] = False
                                config.map.spawnBorder['visible'] = False
                                config.map.spawnBorder['position'] = None
                            break
                        else:
                            config.draw.infoBox['visible'] = False
                            config.draw.infoBox['program'] = None
                elif (15 < x and x < 155) and (175 < y and y < 465):
                    pass
                else:
                    if config.game.state.Map.turn.Init in config.game.states:
                        config.draw.infoBox['visible'] = False
                        config.draw.infoBox['program'] = None
                if (15 < x and x < 130) and (240 < y and y < 465) and config.draw.infoBox['visible']:
                    if type(config.draw.infoBox['program']) is tuple:
                        program = getattr(progs, config.draw.infoBox['program'][0])()
                    else:
                        program = config.draw.infoBox['program']
                    for num, name in zip(range(0, len(program.commands)), program.commands):
                        if num*10+243 < y and y < (num+1)*10+243:
                            config.draw.infoBox['comSelect'] = num
                            config.draw.infoBox['command'] = name
                            break
                        else:
                            config.draw.infoBox['comSelect'] = None
                            config.draw.infoBox['command'] = None
                else:
                    config.draw.infoBox['comSelect'] = None
                    config.draw.infoBox['command'] = None
