#!/usr/bin/python2
from __future__ import print_function, unicode_literals, division
import pygame, pygame.gfxdraw, padlib, copy, programs, demomap as Map, player as Player, misc
from pygame.locals import *

class main(object):
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES,4)
        display = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Haxxit! The h4x0r game!')
        display.fill(pygame.color.THECOLORS['black'])

        map = Map.map()
        player = Player.Programs()
        player.gen(map.spawns, map.enemies)
        game = misc.game()
        draw = misc.draw()
        
        while not game.finished:
            display.fill(pygame.color.THECOLORS['black'])
            # This generates the squares of the board or takes the squares from an array (if already generated)
            map.genBoard(display)
            # This executes before the level has started, ie when selecting what programs you're going to use
            if not game.started:
                map.genSpawns(display, player)
            else: # This executes after the player has started the level, ie when actually engaging in battle
                map.genGame(display, player)
            ##### Generate the sidebar #####
            draw.sidebar(display, game, player, programs)
            pygame.display.update()

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    game.finished = True
                    break
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game.finished = True
                        break
                    elif event.key == K_UP:
                        player.active[map.programBorder['option']].move(player, map, game, programs.dirs.UP)
                    elif event.key == K_DOWN:
                        player.active[map.programBorder['option']].move(player, map, game, programs.dirs.DOWN)
                    elif event.key == K_LEFT:
                        player.active[map.programBorder['option']].move(player, map, game, programs.dirs.LEFT)
                    elif event.key == K_RIGHT:
                        player.active[map.programBorder['option']].move(player, map, game, programs.dirs.RIGHT)
                    else: print(event.key)
                elif event.type == MOUSEMOTION:
                    x, y = event.pos
                    if not game.started and not map.spawnBorder['selected']:
                        for xCoord, yCoord in map.spawns:
                            x1 = (xCoord+1)*35+150
                            y1 = (yCoord+1)*35+15
                            if (x-x1)**2 + (y-y1)**2 <= 5**2:
                                map.spawnBorder['visible'] = True
                                map.spawnBorder['position'] = (xCoord, yCoord)
                                break
                            else:
                                map.spawnBorder['visible'] = False
                                map.spawnBorder['position'] = None
                    elif game.started:
                        if not map.programBorder['selected']:
                            for program in player.active:
                                x1 = (program.sectors[0][0]+1)*35+150
                                y1 = (program.sectors[0][1]+1)*35+15
                                if (x-x1)**2 + (y-y1)**2 <= 10**2:
                                    map.programBorder['visible'] = True
                                    map.programBorder['position'] = (program.sectors[0][0], program.sectors[0][1])
                                    break
                                else:
                                    map.programBorder['visible'] = False
                                    map.programBorder['position'] = None
                    if (15 < x and x < 145) and (15 < y and y < 150):
                        for num in range(1, len(player.programs)+1):
                            if num*12+18 < y and y < (num+1)*12+18:
                                draw.selectBox['visible'] = True
                                draw.selectBox['option'] = num
                                break
                            else:
                                draw.selectBox['visible'] = False
                                draw.selectBox['option'] = 0
                    else:
                        draw.selectBox['visible'] = False
                        draw.selectBox['option'] = 0
                    
                    if (15 < x and x < 130) and (240 < y and y < 465) and draw.infoBox['visible']:
                        program = getattr(programs, draw.infoBox['program'][0])()
                        for num, name in zip(range(0, len(program.commands)), program.commands):
                            if num*10+243 < y and y < (num+1)*10+243:
                                draw.infoBox['comHover'] = num
                                break
                            else:
                                draw.infoBox['comHover'] = None
                    else:
                        draw.infoBox['comHover'] = None

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if not game.started:
                        for xCoord, yCoord in map.spawns:
                            x1 = (xCoord+1)*35+150
                            y1 = (yCoord+1)*35+15
                            if (x-x1)**2 + (y-y1)**2 <= 5**2:
                                map.spawnBorder['selected'] = True
                                draw.selectBox['visible'] = False
                                draw.selectBox['option'] = 0
                                draw.infoBox['visible'] = False
                                draw.infoBox['program'] = None
                                draw.infoBox['comSelect'] = None
                                break
                            elif (15 < x and x < 155) and (15 < y and y < 150):
                                pass
                            else:
                                map.spawnBorder['selected'] = False
                                map.spawnBorder['visible'] = False
                        if (585 < x and x < 635) and (460 < y and y < 475):
                            if not misc.anyEqual(player.active, map.spawns):
                                game.started = True
                    else:
                        for num, program in zip(range(0, len(player.active)),player.active):
                            x1 = (program.sectors[0][0]+1)*35+150
                            y1 = (program.sectors[0][1]+1)*35+15
                            if (x-x1)**2 + (y-y1)**2 <= 10**2 and game.started and player.active[num].moves < player.active[num].speed:
                                map.programBorder['selected'] = True
                                map.programBorder['visible'] = True
                                map.programBorder['position'] = (program.sectors[0][0], program.sectors[0][1])
                                map.programBorder['option'] = num
                                draw.infoBox['visible'] = True
                                draw.infoBox['program'] = program
                                break
                            elif (15 < x and x < 155) and (175 < y and y < 465):
                                pass
                            else:
                                map.programBorder['selected'] = False
                                map.programBorder['visible'] = False
                                map.programBorder['position'] = None
                                draw.infoBox['visible'] = False
                                draw.infoBox['program'] = None
                    if (15 < x and x < 155) and (15 < y and y < 150):
                        for num in range(1, len(player.programs)+1):
                            if (num*12+18 < y and y < (num+1)*12+18) and not draw.infoBox['program'] == player.programs[num-1]:
                                if not map.spawnBorder['selected']:
                                    draw.infoBox['visible'] = True
                                    draw.infoBox['program'] = player.programs[num-1]
                                elif player.programs[num-1][1] > 0:
                                    try: player.active[map.spawns.index(map.spawnBorder['position'])].name
                                    except AttributeError:
                                        player.programs[num-1] = (player.programs[num-1][0], player.programs[num-1][1] - 1, player.programs[num-1][2])
                                        player.active[map.spawns.index(map.spawnBorder['position'])] = getattr(programs, player.programs[num-1][0])([map.spawnBorder['position']])
                                    else:
                                        if type(player.active[map.spawns.index(map.spawnBorder['position'])]) == type(getattr(programs, player.programs[num-1][0])([map.spawnBorder['position']])):
                                            for num in range(0, len(player.programs)):
                                                if player.programs[num][0] == player.active[map.spawns.index(map.spawnBorder['position'])].name:
                                                    player.programs[num] = (player.programs[num][0], player.programs[num][1] + 1, player.programs[num][2])
                                            player.active[map.spawns.index(map.spawnBorder['position'])] = map.spawns[map.spawns.index(map.spawnBorder['position'])]
                                        else:
                                            pass
                                            # DOES NOT WORK
                                            #for num in range(0, len(player.programs)):
                                            #    if player.programs[num][0] == player.active[map.spawns.index(map.spawnBorder['position'])].name:
                                            #        player.programs[num] = (player.programs[num][0], player.programs[num][1] + 1, player.programs[num][2])
                                            #player.programs[num] = (player.programs[num][0], player.programs[num][1] - 1, player.programs[num][2])
                                            #player.active[map.spawns.index(map.spawnBorder['position'])] = getattr(programs, player.programs[num][0])([map.spawnBorder['position']])
                                    map.spawnBorder['selected'] = False
                                    map.spawnBorder['visible'] = False
                                    map.spawnBorder['position'] = None
                                break
                            else:
                                draw.infoBox['visible'] = False
                                draw.infoBox['program'] = None
                    elif (15 < x and x < 155) and (175 < y and y < 465):
                        pass
                    else:
                        draw.infoBox['visible'] = False
                        draw.infoBox['program'] = None
                    if (15 < x and x < 130) and (240 < y and y < 465) and draw.infoBox['visible']:
                        program = getattr(programs, draw.infoBox['program'][0])()
                        for num, name in zip(range(0, len(program.commands)), program.commands):
                            if num*10+243 < y and y < (num+1)*10+243:
                                draw.infoBox['comSelect'] = num
                                draw.infoBox['command'] = name
                                break
                            else:
                                draw.infoBox['comSelect'] = None
                                draw.infoBox['command'] = None
                    else:
                        draw.infoBox['comSelect'] = None
                        draw.infoBox['command'] = None

if __name__=='__main__':
    main()
