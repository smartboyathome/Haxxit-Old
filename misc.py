import padlib, pygame, os, sys, weakref, config, programs
from enum import Enum, EnumValue

class draw():
    selectBox = {'visible': False, 'option': 0}
    infoBox = {'visible': False, 'program': None, 'offset': 0, 'comHover': None, 'comSelect': None, 'command': None}
    attackDict = {'visible': False, 'program': None, 'command': None, 'squares': [], 'coords': []}
    
    def sidebar(self):
        padlib.RoundedRect(config.display, pygame.color.THECOLORS['white'], (5,5,150,470), 15, 2)
        padlib.RoundedRect(config.display, pygame.color.THECOLORS['white'], (15,15,130,150), 10, 1)
        padlib.RoundedRect(config.display, pygame.color.THECOLORS['white'], (15,175,130,290), 10, 1)
        if self.infoBox['visible']:
            if config.game.state.Map.turn.Init in config.game.states.sub:
                pygame.gfxdraw.box(config.display, pygame.rect.Rect(17,(config.player.programs.index(draw.infoBox['program'])+1-draw.infoBox['offset'])*12+18,126,12), pygame.color.THECOLORS['gray20'])
                pygame.gfxdraw.rectangle(config.display, pygame.rect.Rect(17,(config.player.programs.index(draw.infoBox['program'])+1-draw.infoBox['offset'])*12+18,126,12), pygame.color.THECOLORS['gray20'])
                program = getattr(programs, self.infoBox['program'][0])()
            else:
                program = self.infoBox['program']
            pygame.gfxdraw.aacircle(config.display, 30, 192, 10, pygame.Color(pygame.color.THECOLORS[program.color][0], pygame.color.THECOLORS[program.color][1], pygame.color.THECOLORS[program.color][2], pygame.color.THECOLORS[program.color][3]))
            pygame.gfxdraw.filled_circle(config.display, 30, 192, 10, pygame.Color(pygame.color.THECOLORS[program.color][0], pygame.color.THECOLORS[program.color][1], pygame.color.THECOLORS[program.color][2], pygame.color.THECOLORS[program.color][3]))
            config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 12).render('Moves left: '+str(program.speed-program.moves), 1, pygame.Color(255,255,255,255)), (47,180))
            config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 12).render('Max Size: '+str(program.maxSize), 1, pygame.Color(255,255,255,255)), (47,188))
            if program.sectors != None:
                config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 12).render('Current Size: '+str(len(program.sectors)), 1, pygame.Color(255,255,255,255)), (47,196))
            config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 24).render(draw.infoBox['program'][0] if type(config.draw.infoBox['program']) is tuple else draw.infoBox['program'].name, 1, pygame.Color(255,255,255,255)), (20, 207))
            config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 18).render('Commands', 1, pygame.Color(255,255,255,255)), (20, 227))
            if self.infoBox['comSelect'] != None:
                pygame.gfxdraw.box(config.display, pygame.rect.Rect(17,draw.infoBox['comSelect']*10+243,126,10), pygame.color.THECOLORS['gray20'])
                pygame.gfxdraw.rectangle(config.display, pygame.rect.Rect(17,draw.infoBox['comSelect']*10+243,126,10), pygame.color.THECOLORS['gray20'])
                offset = 375
                if program.commands[draw.infoBox['command']][0] > 1:
                    config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render('Range: '+str(program.commands[draw.infoBox['command']][0]), 1, pygame.Color(255,255,255,255)), (17,offset))
                    offset = offset + 10
                text = program.commands[draw.infoBox['command']][2].split('\n')
                for line in text:
                    config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render(line, 1, pygame.Color(255,255,255,255)), (17,text.index(line)*10+offset))
            if self.infoBox['comHover'] != None:
                pygame.gfxdraw.box(config.display, pygame.rect.Rect(17,draw.infoBox['comHover']*10+243,126,10), pygame.color.THECOLORS['gray32'])
                pygame.gfxdraw.rectangle(config.display, pygame.rect.Rect(17,draw.infoBox['comHover']*10+243,126,10), pygame.color.THECOLORS['gray32'])
            for num, command in zip(range(0, len(program.commands)), program.commands):
                config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render(command, 1, pygame.Color(255,255,255,255)), (32, num*10+242))
        if self.selectBox['visible']:
            pygame.gfxdraw.box(config.display, pygame.rect.Rect(17,draw.selectBox['option']*12+18,126,12), pygame.color.THECOLORS['gray32'])
            pygame.gfxdraw.rectangle(config.display, pygame.rect.Rect(17,draw.selectBox['option']*12+18,126,12), pygame.color.THECOLORS['gray32'])
        if config.game.state.Map.turn.Init in config.game.states.sub:
            for program in config.player.programs:
                config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render(program[0], 1, pygame.Color(255,255,255,255)), (18, (config.player.programs.index(program)+1)*12+18))
                config.display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render('x'+str(program[1]), 1, pygame.Color(255,255,255,255)), (128, (config.player.programs.index(program)+1)*12+18))

    def attack(self):
        if self.attackDict['visible']:
            if self.attackDict['squares'] == []:
                dist = self.attackDict['program'].commands[self.attackDict['command']][0]
                coord = self.attackDict['program'].sectors[0]
                start = [coord[0]-dist, coord[1]-dist]
                offset = [dist,0,False] # [offset_x, offset_y, reverse]
                square_count = 1
                square_tmp = 0
                finished = False
                squares = []
                print coord
                while not finished:
                    cur = (start[0]+offset[0]+square_tmp, start[1]+offset[1])
                    print(cur, square_tmp, square_count)
                    if config.map.squareAvail(cur[0], cur[1]) and \
                       not config.player.squareTaken(cur[0], cur[1], True):
                        squares.append(pygame.rect.Rect((cur[0]+1)*35+135, (cur[1]+1)*35, 30, 30))
                    if not square_tmp == square_count-1:
                        square_tmp += 1
                    else:
                        if offset[0] == 0:
                            offset[2] = True
                        if not offset[2]:
                            square_count += 2
                            offset[0] -= 1
                        else:
                            square_count -= 2
                            offset[0] += 1
                            if offset[0] > dist:
                                finished = True
                        square_tmp = 0
                        offset[1] += 1
                self.attackDict['squares'] = squares
            for square in self.attackDict['squares']:
                pygame.gfxdraw.box(config.display, square, (127, 0, 0, 127))
                pygame.gfxdraw.rectangle(config.display, square, pygame.color.THECOLORS['red'])

class stateVal(EnumValue):
    def __init__(self, enumtype, index, key):
        super(stateVal, self).__init__(enumtype, index, key)
    # These functions just add support for adding/removing multiple properties
    def add(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
    def remove(self, *args):
        for arg in args:
            if type(arg) is str:
                delattr(self, arg)

class stateEnum(Enum):
    def __init__(self, *args, **kwargs):
        kwargs['value_type'] = stateVal
        super(stateEnum, self).__init__(*args, **kwargs)
        def_props = kwargs.get('def_props')
        if def_props != None and type(def_props) == list or type(def_props) == tuple or type(def_props) == str:
            for i in self:
                if type(def_props) == str: setattr(i, def_props, None)
                else:
                    for prop in def_props:
                        setattr(i, prop, None)
        

class stateSet():
    def __init__(self, gameState=None, subState=None):
        self.game = gameState
        self.sub = set()
        if subState in gameState.turn or subState in gameState.draw:
            self.sub.add(subState)
    def add(self, *args):
        for arg in args:
            if not type(arg) is stateVal: continue
            if arg in config.game.state: self.game = arg
            elif arg.key in self.game.turn:
                for i in self.game.turn:
                    if i in self.sub:
                        self.sub.remove(i)
                self.sub.add(arg)
    def remove(self, *args):
        for arg in args:
            if type(arg) is stateVal: name = arg.key
            elif type(arg) is str: name = arg
            else: continue
    def __contains__(self, value):
        if type(value) is str:
            if self.game.key == value: return True
            for i in self.sub: 
                if i.key == value: return True
            return False
        elif type(value) is stateVal:
            if self.game == value: return True
            for i in self.sub:
                if i == value: return True
            return False
        else: return False

class game():
    state = stateEnum('Intro', 'Menu', 'Network', 'Map', 'Quit')
    def __init__(self):
        # Initializing the linking proess between state enums.
        self.state.Map.add(turn=stateEnum('Init', 'Player', 'Enemy'), draw=stateEnum('Sidebar', 'ProgramBorder', 'SpawnBorder', 'InfoBox', 'SelectBox', 'Attack'))
        self.state.Map.draw.Sidebar.add(visible=False, option=0)
        self.state.Map.draw.ProgramBorder.add(visible=False, selected=False, position=None, option=0)
        self.state.Map.draw.SpawnBorder.add(visible=False, selected=False, position=None)
        self.state.Map.draw.InfoBox.add(visible=False, program=None, offset=0, comHover=None, comSelect=None, command=None)
        self.state.Map.draw.SelectBox.add(visible=False, option=0)
        self.state.Map.draw.Attack.add(visible=False, program=None, command=None, squares=[], coords=[])
        self.states = stateSet(self.state.Map, self.state.Map.turn.Init)

a = 99
def sparsePrint(obj, b=99):
    global a
    a = b
    if a == b:
        print(obj)
        a = 0
    else: a += 1

def anyEqual(list1, list2):
    for item in list1:
        if item == list2[list1.index(item)]:
            return True
    return False
