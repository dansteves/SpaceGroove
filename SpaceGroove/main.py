import pygame
from pygame.locals import *
from HelpLevel.helproom import HelpRoom
from SpaceGrooveLevel.spaceroom import SpaceRoom
from SpaceGrooveLevel2.spaceroom2 import SpaceRoom2
from SpaceGrooveLevel3.spaceroom3 import SpaceRoom3
from SpaceGrooveLevel4.spaceroom4 import SpaceRoom4
from SpaceGrooveLevel5.spaceroom5 import SpaceRoom5
from EndLevel.endroom import EndRoom

screensize = (800,600)
def main():
    pygame.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption('Space Groove')
    # Loading screen
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Loading...", 1, (50, 100, 150))
        textrec = text.get_rect()
        textrec.center = screen.get_rect().center
        screen.blit(text, textrec)
    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(1)

    # Create resources.  May want to do this later,
    # as each level is accomplished.  Slows loading here.
    helproom = HelpRoom(screen)
    spaceroom = SpaceRoom(screen)
    spaceroom2 = SpaceRoom2(screen)
    spaceroom3 = SpaceRoom3(screen)
    spaceroom4 = SpaceRoom4(screen)
    spaceroom5 = SpaceRoom5(screen)
    endroom = EndRoom(screen)
    
    currentroom = helproom
    
    while 1:
        clock.tick(30)
        events = pygame.event.get();
        for event in events:
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN :
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_F1:
                    currentroom = helproom
                elif event.key == K_F2:
                    currentroom = spaceroom
                elif event.key == K_F3:
                    currentroom = spaceroom2
                elif event.key == K_F4:
                    currentroom = spaceroom3
                elif event.key == K_F5:
                    currentroom = spaceroom4
                elif event.key == K_F6:
                    currentroom = spaceroom5
                elif event.key == K_F7:
                    currentroom = endroom
                elif event.key == K_SPACE:
                    if currentroom == helproom:
                        currentroom = spaceroom
                    elif currentroom == endroom:
                        return

        evnum = currentroom.run(events)
        if evnum == 1:
            currentroom.reset()
            currentroom = spaceroom2
        if evnum == 2:
            currentroom.reset()
            currentroom = spaceroom3
        if evnum == 3:
            currentroom.reset()
            currentroom = spaceroom4
        if evnum == 4:
            currentroom.reset()
            currentroom = spaceroom5
        if evnum == 5:
            currentroom.reset()
            currentroom = endroom

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
