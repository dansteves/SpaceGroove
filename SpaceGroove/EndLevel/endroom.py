import pygame
from pygame.locals import *

class EndRoom:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(screen.get_size())
        pygame.draw.rect(self.background,(50,50,50),self.background.get_rect())
        self.font = pygame.font.Font(None, 35)
        for i, txt in enumerate(
            ("Thank you for playing!",
             "",
             "Made by Daniel Stevens",
             "",
             "",
             "",
             "",
             "",
             "Press Space or ESC to exit.")):
            self.textout(txt, 100+i*50)

    def textout(self, text, y):
        rtext = self.font.render(text,1,(200,200,200))
        textrec = rtext.get_rect()
        textrec.centerx = self.background.get_rect().centerx
        textrec.centery = y
        self.background.blit(rtext, textrec)
        
    def reset(self): pass

    def run(self, events):
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        return False
