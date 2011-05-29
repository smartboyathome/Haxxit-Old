#!/usr/bin/python2
from __future__ import print_function, unicode_literals, division
import pygame, pygame.gfxdraw, padlib, copy, programs, demomap as Map, player as Player, misc, config
from pygame.locals import *

class main(object):
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES,4)
        pygame.display.set_caption('Haxxit! The h4x0r game!')
        config.display = pygame.display.set_mode((640, 480))
        config.display.fill(pygame.color.THECOLORS['black'])

        config.map = Map.map()
        config.player = Player.Programs()
        config.player.gen()
        config.game = misc.game()
        config.draw = misc.draw()
        
        while not config.game.state.Quit in config.game.states:
            ##### Draw the game #####
            config.display.fill(pygame.color.THECOLORS['black'])
            # This generates the squares of the board or takes the squares from an array (if already generated)
            config.map.genBoard()
            # This executes before the level has started, ie when selecting what programs you're going to use
            if config.game.state.Map.turn.Init in config.game.states:
                config.map.genSpawns()
            else: # This executes after the player has started the level, ie when actually engaging in battle
                config.map.genGame()
            ##### Generate the sidebar #####
            config.draw.sidebar()
            ##### Draw the attack, if attacking #####
            config.draw.attack()
            ##### End drawing, update screen #####
            pygame.display.update()
            ##### Run Events #####
            config.player.events()

if __name__=='__main__':
    main()
