import os, pygame
from pygame.locals import *

def _loadSound(name, folder=os.path.join("SpaceGrooveLevel2", "data", "sounds")):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        sound = NoneSound()
    else:
        fullname=os.path.join(folder, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error as message:
            print ("Cannot load sound:", fullname)
            raise SystemExit(message)
        return sound

def _loadImage(name, folder=os.path.join("SpaceGrooveLevel2", "data","images"),colorkey=-1):
    fullname = os.path.join(folder, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print ("Cannot load image:", fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image

def _loadSpritesheet(name,
                    start = (0,0),
                    imagesize=(16,16),
                    count=8,
                    folder=os.path.join("SpaceGrooveLevel2", "data","images")):
    spritesheet = _loadImage(name, folder, colorkey=None)
    images = []
    for row in range(count):
        image = pygame.Surface(imagesize).convert()
        x = start[0] + row*imagesize[0]
        y = start[1]
        image.blit(spritesheet, (0,0), ((x,y),imagesize))
        image.set_colorkey(image.get_at((0,0)))
        images.append(image)
    return images

class _ResourceManager:
    def __init__(self,
                 imgpath=os.path.join("SpaceGrooveLevel2", "data","images"),
                 sndpath=os.path.join("SpaceGrooveLevel2", "data","sounds")):
        self.imgpath = imgpath
        self.sndpath = sndpath
        self.initialized = False
        
    # can't initialize until after pygame display is initialized:
    def initialize(self):
        if self.initialized:
            return self
        self.initialized = True
        self.loseSound = _loadSound('youlose.wav', self.sndpath)
        self.explosionSound = _loadSound('explosion.wav', self.sndpath)
        self.levelSound = _loadSound('level.wav', self.sndpath)
        self.missileSound = _loadSound('missile.wav', self.sndpath)
        self.thrustSound = _loadSound('thrust.wav', self.sndpath)
        
        self.explosion = _loadSpritesheet('explosion.png',
                                             (0,0),
                                             (75,75),
                                             9)
        self.nebula = _loadImage('nebula.jpg', self.imgpath, colorkey=None)
        #Scale background to full screen
        self.nebula = pygame.transform.scale(self.nebula, (800,600))
        self.missile = _loadImage('missile.bmp', self.imgpath)
        self.bigAsteroid = _loadImage('asteroid_big.bmp', self.imgpath)
        self.medAsteroid = _loadImage('asteroid_med.bmp', self.imgpath)
        self.smallAsteroid = _loadImage('asteroid_small.bmp', self.imgpath)
        self.ship = _loadSpritesheet('ship.png',
                                    (0,0), (34,34), 36,
                                     self.imgpath)
        self.shipflame = _loadSpritesheet('shipflame.png',
                                         (0,0), (40,40), 36,
                                          self.imgpath)
        return self

# singleton interface, can't initialize until later:
_resourcemanager = _ResourceManager()
def ResourceManager():
    return _resourcemanager

#### Some tests:
if __name__ == "__main__":
    try:
        pygame.init()
        screen = pygame.display.set_mode((40*36, 480))
        # now we can initialize the resource manager:
        rm = ResourceManager().initialize()
        pygame.mixer.music.load(os.path.join("SpaceGrooveLevel2", "data","music","theme.mid"))
        pygame.mixer.music.play(-1)

        rm.explosionSound.play()
        done = False
        while not(done):
            screen.fill((0,0,255))
            screen.blit(rm.nebula, (0,0))
            for i,img in enumerate(rm.explosion):
                screen.blit(img, (i*75, 0))
            for i,img in enumerate(rm.ship):
                screen.blit(img, (i*34, 75))
            for i,img in enumerate(rm.shipflame):
                screen.blit(img, (i*40, 75+34))
            screen.blit(rm.bigAsteroid, (0, 75+40+34))
            screen.blit(rm.medAsteroid, (100, 75+40+34))
            screen.blit(rm.smallAsteroid, (200, 75+40+34))
                
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True
    finally:
        pygame.quit()

