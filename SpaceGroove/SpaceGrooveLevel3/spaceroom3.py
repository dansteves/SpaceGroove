#/usr/bin/env python
"""
Cloned from a GameMaker game, which I cloned from a pygame game, Astrocrash
Geoffrey Matthews
2017
"""

import os, pygame
from pygame.locals import *

from SpaceGrooveLevel3.objects import ObjectManager, Ship
from SpaceGrooveLevel3.resources import ResourceManager

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
    
class SpaceRoom3:
    def __init__(self, screen):
        self.screen = screen
        self.done = False

        # initialize resources before objects
        self.rm = ResourceManager().initialize()
        self.om = ObjectManager().initialize()
        self.ship = self.om.ships.sprites()[0]
        pygame.mixer.music.load(os.path.join("SpaceGrooveLevel3","data","music","theme.wav"))
        pygame.mixer.music.play(-1)
    
    def reset(self):
        self.done = False
        
    def run(self, events):
        if self.done: return 3
        # start the game loop
        clock = pygame.time.Clock()
        #done = False
        if not(self.done):
            clock.tick(30)

            # check user events
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.ship.left()
            if keys[K_RIGHT]:
                self.ship.right()
            if keys[K_UP]:
                self.ship.accelerate()
            if not keys[K_UP]:
                self.ship.coast()
            if keys[K_SPACE]:
                self.ship.fire()
            if keys[K_z]:
                self.ship.fire()

            # update objects
            self.om.objects.update()

            # draw everything
            self.screen.blit(ResourceManager().nebula, (0,0))
            self.om.objects.draw(self.screen)
            pygame.display.flip() 

            # poll keyboard
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 5
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return 5
                elif event.type == USEREVENT+1:
                    return 5
                elif event.type == USEREVENT: # game over
                    self.done = True
