import copy, pygame, misc, padlib, config

class funcs():
    spawnBorder = {'visible': False, 'selected': False, 'position': None}
    programBorder = {'visible': False, 'selected': False, 'position': None, 'option': 0}
    squares = []
    
    def squareAvail(self, x, y):
        if x < 0 or y < 0: return False
        else: return self.layout[y][x] != 0
    
    def genBoard(self):
        try: self.squares[0]
        except IndexError:
            for yCoord in range(1, len(self.layout)+1):
                y = yCoord*35
                row = []
                for xCoord in range(1, len(self.layout[yCoord-1])+1):
                    if self.layout[yCoord-1][xCoord-1] == 1:
                        x = xCoord*35+135
                        row.append(pygame.rect.Rect(x, y, 30, 30))
                        pygame.gfxdraw.box(config.display, row[-1], pygame.color.THECOLORS['white'])
                        pygame.gfxdraw.rectangle(config.display, row[-1], pygame.color.THECOLORS['white'])
                    else:
                        row.append(None)
                self.squares.append(copy.deepcopy(row))
        else:
            for row in self.squares:
                for square in row:
                    if square != None:
                        pygame.gfxdraw.box(config.display, square, pygame.color.THECOLORS['white'])
                        pygame.gfxdraw.rectangle(config.display, square, pygame.color.THECOLORS['white'])

    def genSpawns(self):
        for xCoord, yCoord in self.spawns:
            if config.player.active[self.spawns.index((xCoord, yCoord))] == (xCoord, yCoord):
                pygame.gfxdraw.aacircle(config.display, (xCoord+1)*35+150, (yCoord+1)*35+15, 5, pygame.Color(127, 127, 127, 255))
                pygame.gfxdraw.filled_circle(config.display, (xCoord+1)*35+150, (yCoord+1)*35+15, 5, pygame.Color(127, 127, 127, 255))
            else:
                r, g, b, a = pygame.color.THECOLORS[config.player.active[self.spawns.index((xCoord, yCoord))].color]
                pygame.gfxdraw.aacircle(config.display, (xCoord+1)*35+150, (yCoord+1)*35+15, 10, pygame.Color(r, g, b, a))
                pygame.gfxdraw.filled_circle(config.display, (xCoord+1)*35+150, (yCoord+1)*35+15, 10, pygame.Color(r, g, b, a))
        if self.spawnBorder['visible'] or self.spawnBorder['selected']:
            for i in range(8,10):
                pygame.gfxdraw.aacircle(config.display, (self.spawnBorder['position'][0]+1)*35+150, (self.spawnBorder['position'][1]+1)*35+15, i, pygame.Color(127, 127, 127, 255))
        if not misc.anyEqual(config.player.active, self.spawns):
            padlib.RoundedRect(config.display, pygame.color.THECOLORS['white'], (585,460,50,15), 3, 1)
            config.display.blit(pygame.font.Font('visitor2.ttf', 12).render('Start', 1, pygame.Color(255,255,255,255)), (595,463))
        for enemy in config.player.enemies:
            self.renderProgram(enemy)

    def genGame(self):
        for program in config.player.active + config.player.enemies:
            self.renderProgram(program)
    
    def renderProgram(self, program):
        r, g, b, a = pygame.color.THECOLORS[program.color]
        for xCoord, yCoord in program.sectors:
            pygame.gfxdraw.aacircle(config.display, (xCoord+1)*35+150, (yCoord+1)*35+15, 10, pygame.Color(r, g, b, a))
            pygame.gfxdraw.filled_circle(config.display, (xCoord+1)*35+150, (yCoord+1)*35+15, 10, pygame.Color(r, g, b, a))
            try: program.sectors[program.sectors.index((xCoord, yCoord))+1]
            except IndexError: pass
            else:
                xCoord2, yCoord2 = program.sectors[program.sectors.index((xCoord, yCoord))+1]
                xDist, yDist = (xCoord - xCoord2, yCoord - yCoord2)
                if yDist == 0 and xDist > 0:
                    rect = pygame.rect.Rect((xCoord2+1)*35+150, (yCoord+1)*35+12, 45, 6)
                elif yDist == 0 and xDist < 0:
                    rect = pygame.rect.Rect((xCoord+1)*35+150, (yCoord+1)*35+12, 45, 6)
                elif xDist == 0 and yDist > 0:
                    rect = pygame.rect.Rect((xCoord+1)*35+147, (yCoord2+1)*35+15, 6, 35)
                elif xDist == 0 and yDist < 0:
                    rect = pygame.rect.Rect((xCoord+1)*35+147, (yCoord+1)*35+15, 6, 35)
                pygame.gfxdraw.box(config.display, rect, pygame.color.THECOLORS[program.color])
                pygame.gfxdraw.rectangle(config.display, rect, pygame.color.THECOLORS[program.color])
        if self.programBorder['visible'] or self.programBorder['selected']:
            for i in range(9,11):
                pygame.gfxdraw.aacircle(config.display, (self.programBorder['position'][0]+1)*35+150, (self.programBorder['position'][1]+1)*35+15, i, pygame.Color(127, 127, 127, 255))
