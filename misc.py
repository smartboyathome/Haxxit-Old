import padlib, pygame, os, sys

class draw():
    selectBox = {'visible': False, 'option': 0}
    infoBox = {'visible': False, 'program': None, 'offset': 0, 'comHover': None, 'comSelect': None, 'command': None}
    def sidebar(self, display, game, player, programs):
        padlib.RoundedRect(display, pygame.color.THECOLORS['white'], (5,5,150,470), 15, 2)
        padlib.RoundedRect(display, pygame.color.THECOLORS['white'], (15,15,130,150), 10, 1)
        padlib.RoundedRect(display, pygame.color.THECOLORS['white'], (15,175,130,290), 10, 1)
        if self.infoBox['visible']:
            if not game.started:
                pygame.gfxdraw.box(display, pygame.rect.Rect(17,(player.programs.index(draw.infoBox['program'])+1-draw.infoBox['offset'])*12+18,126,12), pygame.color.THECOLORS['gray20'])
                pygame.gfxdraw.rectangle(display, pygame.rect.Rect(17,(player.programs.index(draw.infoBox['program'])+1-draw.infoBox['offset'])*12+18,126,12), pygame.color.THECOLORS['gray20'])
                program = getattr(programs, self.infoBox['program'][0])()
            else:
                print(True)
                program = self.infoBox['program']
            pygame.gfxdraw.aacircle(display, 30, 192, 10, pygame.Color(pygame.color.THECOLORS[program.color][0], pygame.color.THECOLORS[program.color][1], pygame.color.THECOLORS[program.color][2], pygame.color.THECOLORS[program.color][3]))
            pygame.gfxdraw.filled_circle(display, 30, 192, 10, pygame.Color(pygame.color.THECOLORS[program.color][0], pygame.color.THECOLORS[program.color][1], pygame.color.THECOLORS[program.color][2], pygame.color.THECOLORS[program.color][3]))
            display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 12).render('Moves: '+str(program.speed), 1, pygame.Color(255,255,255,255)), (47,180))
            display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 12).render('Max Size: '+str(program.maxSize), 1, pygame.Color(255,255,255,255)), (47,188))
            if program.sectors != None:
                display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 12).render('Current Size: '+str(len(program.sectors)), 1, pygame.Color(255,255,255,255)), (47,196))
            display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 24).render(draw.infoBox['program'][0], 1, pygame.Color(255,255,255,255)), (20, 207))
            display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 18).render('Commands', 1, pygame.Color(255,255,255,255)), (20, 227))
            if self.infoBox['comSelect'] != None:
                pygame.gfxdraw.box(display, pygame.rect.Rect(17,draw.infoBox['comSelect']*10+243,126,10), pygame.color.THECOLORS['gray20'])
                pygame.gfxdraw.rectangle(display, pygame.rect.Rect(17,draw.infoBox['comSelect']*10+243,126,10), pygame.color.THECOLORS['gray20'])
                offset = 375
                if program.commands[draw.infoBox['command']][0] > 1:
                    display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render('Range: '+str(program.commands[draw.infoBox['command']][0]), 1, pygame.Color(255,255,255,255)), (17,offset))
                    offset = offset + 10
                text = program.commands[draw.infoBox['command']][2].split('\n')
                for line in text:
                    display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render(line, 1, pygame.Color(255,255,255,255)), (17,text.index(line)*10+offset))
            if self.infoBox['comHover'] != None:
                pygame.gfxdraw.box(display, pygame.rect.Rect(17,draw.infoBox['comHover']*10+243,126,10), pygame.color.THECOLORS['gray32'])
                pygame.gfxdraw.rectangle(display, pygame.rect.Rect(17,draw.infoBox['comHover']*10+243,126,10), pygame.color.THECOLORS['gray32'])
            for num, command in zip(range(0, len(program.commands)), program.commands):
                display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render(command, 1, pygame.Color(255,255,255,255)), (32, num*10+242))
        if self.selectBox['visible']:
            pygame.gfxdraw.box(display, pygame.rect.Rect(17,draw.selectBox['option']*12+18,126,12), pygame.color.THECOLORS['gray32'])
            pygame.gfxdraw.rectangle(display, pygame.rect.Rect(17,draw.selectBox['option']*12+18,126,12), pygame.color.THECOLORS['gray32'])
        if not game.started:
            for program in player.programs:
                display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render(program[0], 1, pygame.Color(255,255,255,255)), (18, (player.programs.index(program)+1)*12+18))
                display.blit(pygame.font.Font(os.path.join(os.path.dirname(__file__), 'visitor2.ttf'), 14).render('x'+str(program[1]), 1, pygame.Color(255,255,255,255)), (128, (player.programs.index(program)+1)*12+18))

class game():
    started = False
    finished = False

def anyEqual(list1, list2):
    for item in list1:
        if item == list2[list1.index(item)]:
            return True
    return False
