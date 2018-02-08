import pygame, math, random
from SpaceGrooveLevel.resources import ResourceManager
from pygame.locals import *


glasteroids1 = 0
count = 0
class LoseMessage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if pygame.font:
            font = pygame.font.Font(None, 128)
            self.image = font.render("You Lose!", 1, (255, 0, 0))
            screen = pygame.display.get_surface()
            self.rect = self.image.get_rect()
            self.rect.center = screen.get_rect().center

class WinMessage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if pygame.font:
            font = pygame.font.Font(None, 128)
            self.image = font.render("You Win!", 1, (0, 200, 0))
            screen = pygame.display.get_surface()
            self.rect = self.image.get_rect()
            self.rect.center = screen.get_rect().center
        
class Explosion(pygame.sprite.Sprite):
    """Explosion sprite.  Kills self after animation is done."""
    def __init__(self,position):
        rm = ResourceManager()
        pygame.sprite.Sprite.__init__(self)
        rm.explosionSound.play()
        self.images = rm.explosion
        self.rect = self.images[0].get_rect()
        self.rect.center = position
        self.nframes = len(self.images)
        self.frame = 0
        self.image = self.images[0]
        self.aspeed = 0.5
        
    def update(self):
        self.frame = (self.frame+self.aspeed)
        if self.frame >= self.nframes:
            self.kill()
        else:
            self.image = self.images[int(self.frame)]

class MOB(pygame.sprite.Sprite):
    """Abstract superclass for mobile sprites"""
    def __init__(self, position, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.velocity = velocity

    def update(self):
        w, h = pygame.display.get_surface().get_size()
        x,y = self.position
        u,v = self.velocity
        newx = x+u
        newy = y+v
        self.rect.center = (int(newx), int(newy))
        if self.rect.right < 0:
            newx += w + self.rect.width
        if self.rect.left > w:
            newx -= w + self.rect.width
        if self.rect.bottom < 0:
            newy += h + self.rect.height
        if self.rect.top > h:
            newy -= h + self.rect.height
        self.position = (newx, newy)
        self.rect.center = (int(newx), int(newy))

class Missile(MOB):
    def __init__(self, position, velocity, counter=100):
        MOB.__init__(self, position, velocity)
        rm = ResourceManager()
        rm.missileSound.play()
        self.image = rm.missile
        self.rect = rm.missile.get_rect()
        self.counter = counter
        
    def update(self):
        om = ObjectManager()
        rm = ResourceManager()
        MOB.update(self)
        self.counter -= 1
        if self.counter < 0:
            self.kill()
        #check for collisions
        asteroid = pygame.sprite.spritecollideany(self, om.asteroids)
        if asteroid:
            self.kill()
            asteroid.kill()
            global glasteroids1
            glasteroids1 -= 1
            rm.explosionSound.play()
            if type(asteroid) == BigAsteroid:
                for x in range(2):
                    glasteroids1 += 1
                    om.addAsteroid(
                        MedAsteroid(asteroid.position,
                                    (-2+4*random.random(),
                                     -2+4*random.random())))
            elif type(asteroid) == MedAsteroid:
                for x in range(2):
                    glasteroids1 += 1
                    om.addAsteroid(
                        SmallAsteroid(asteroid.position,
                                      (-3+6*random.random(),
                                       -3+6*random.random())))

class BigAsteroid(MOB):
    def __init__(self, position, velocity):
        MOB.__init__(self, position, velocity)
        rm = ResourceManager()
        self.image = rm.bigAsteroid
        self.rect = rm.bigAsteroid.get_rect()
        
class MedAsteroid(MOB):
    def __init__(self, position, velocity):
        MOB.__init__(self, position, velocity)
        rm = ResourceManager()
        self.image = rm.medAsteroid
        self.rect = rm.medAsteroid.get_rect()
        
class SmallAsteroid(MOB):
    def __init__(self, position, velocity):
        MOB.__init__(self, position, velocity)
        rm = ResourceManager()
        self.image = rm.smallAsteroid
        self.rect = rm.smallAsteroid.get_rect()

class Ship(MOB):
    def __init__(self):
        x,y = pygame.display.get_surface().get_size()
        MOB.__init__(self, (x/2, y/2), (0,0))
        rm = ResourceManager()
        self.thrustSound = rm.thrustSound
        self.friction = 0.99
        self.acceleration = 0.25
        self.images = rm.ship
        self.ship = rm.ship
        self.shipflame = rm.shipflame
        self.rect = self.images[0].get_rect()
        self.heading = 0.0
        self.image = self.images[0]
        self.velocity = (0.0, 0.0)
        self.thrustSoundPlaying = False
        self.fireTimer = 0

    def left(self):
        self.heading += 1.5
    def right(self):
        self.heading -= 1.5

    def accelerate(self):
        if not self.thrustSoundPlaying:
            self.thrustSoundPlaying = True
            self.thrustSound.play(-1)
        self.images = self.shipflame
        self.rect = self.images[0].get_rect()
        u,v = self.velocity
        du = self.acceleration * math.cos(math.pi*self.heading/18.0)
        dv = self.acceleration * math.sin(math.pi*self.heading/18.0)
        self.velocity = (u+du, v-dv)

    def coast(self):
        self.thrustSoundPlaying = False
        self.thrustSound.fadeout(500)
        self.images = self.ship
        self.rect = self.images[0].get_rect()

    def fire(self):
        if self.fireTimer > 0:
            return
        else:
            self.fireTimer = 20
        om = ObjectManager()
        x,y = self.position
        u,v = self.velocity
        du = 5 * math.cos(math.pi*self.heading/18.0)
        dv = 5 * math.sin(math.pi*self.heading/18.0)
        om.addMissile(Missile(self.position, (u+du, v-dv)))
        
    def update(self):
        #update timers
        self.fireTimer = max(self.fireTimer-1, 0)
        om = ObjectManager()
        #update image
        self.image = self.images[int(self.heading)%36]
        #update velocity
        u,v = self.velocity
        self.velocity = (u*self.friction, v*self.friction)
        #update position
        MOB.update(self)
        #check for collisions
        asteroids = om.asteroids
        global glasteroids1
        if pygame.sprite.spritecollideany(self, asteroids):
            # game over
            self.kill()
            om.addExplosion(Explosion(self.position))
            om.addLoseMessage()
            ResourceManager().loseSound.play()
            #pygame.quit()
            pygame.time.set_timer(USEREVENT+1, 2000)
        if glasteroids1 <= 0:
            self.kill()
            om.addExplosion(Explosion(self.position))
            om.addWinMessage()
            ResourceManager().loseSound.play()
            pygame.time.set_timer(USEREVENT, 2000)

class _ObjectManager:
    def __init__(self):
        self.objects = pygame.sprite.RenderPlain()
        self.asteroids = pygame.sprite.RenderPlain()
        self.missiles = pygame.sprite.RenderPlain()
        self.ships = pygame.sprite.RenderPlain()
        self.explosions = pygame.sprite.RenderPlain()
        self.initialized = False

    # can't initalize until after pygame screen initialized:
    def initialize(self, numAsteroids = 4):
        if self.initialized:
            return self
        self.initialized = True
        self.addShip(Ship())
        global glasteroids1
        glasteroids1 = numAsteroids

        w,h = pygame.display.get_surface().get_size()
        x,y = w*0.5, h*0.5
        dx,dy = x*0.75, y*0.75
        for n in range(numAsteroids):
            angle = 2.0*math.pi*float(n)/float(numAsteroids)
            sinAngle = math.sin(angle)
            cosAngle = math.cos(angle)
            self.addAsteroid(
                BigAsteroid((int(x + cosAngle*dx), int(y + sinAngle*dy)),
                            (-1+1*random.random(), -1+1*random.random())))
        return self

    def update(self):
        self.objects.update()

    def draw(self, screen):
        self.objects.draw(screen)

    def addShip(self, ship):
        self.ships.add(ship)
        self.objects.add(ship)
        
    def addAsteroid(self, ast):
        self.asteroids.add(ast)
        self.objects.add(ast)

    def addMissile(self, miss):
        self.missiles.add(miss)
        self.objects.add(miss)

    def addExplosion(self, expl):
        self.explosions.add(expl)
        self.objects.add(expl)

    def addLoseMessage(self):
        self.objects.add(LoseMessage())

    def addWinMessage(self):
        self.objects.add(WinMessage())

# singleton interface:
_objectmanager = _ObjectManager()
def ObjectManager():
    return _objectmanager
        

        
