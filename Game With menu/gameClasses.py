import keystore
import sys
import os
import math
import random
import pygame
import pygame.mixer
import euclid

#colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

#collision variables
NO_COLLISION = 0
HIT_TOP = 1
HIT_BOTTOM = 2
HIT_RIGHT = 3
HIT_LEFT = 4
HIT_CORNER = 5

#bullet variables -- can put these into weapon class when it's made
BULLET_DELAY = .2
BULLET_RANGE = 5

#environment variables
drag = euclid.Vector2(50.0, 0.0)
screen_size = screen_width, screen_height = 1000, 500


#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
#******************************************************SpritePlayer*********************************************************************************************
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
class SpritePlayer(pygame.sprite.Sprite):

    def __init__(self, startPos, height, length, screen, velocity=euclid.Vector2(0.0, 0.0), accel=euclid.Vector2(0.0, 0.0), width=1):
                # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.startPos = startPos
        self.height = height
        self.length = length
        self.screen = screen
        self.velocity = velocity
        self.accel = accel
        self.width = width

        self.image = pygame.transform.scale(pygame.image.load("spaceman.png").convert_alpha(), [length, height])
        self.rect = self.image.get_rect()
        self.rect.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)
        self.right = True  # change the direction the image is facing

#*************************************************************************************************
#*************************************************************************************************
#used to blit the image
    def update(self):
        self.screen.blit(pygame.transform.flip(self.image, not self.right, 0), (self.rect))
        self.rect.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)

#*************************************************************************************************
#*************************************************************************************************
#moves the object
    def move(self, dtime):
        self.startPos += self.velocity * dtime + 0.5 * (self.accel * (dtime ** 2))
        self.velocity += self.accel * dtime
        self.velocity.x -= self.velocity.x * drag.x * dtime
        self.velocity.y -= self.velocity.y * drag.y * dtime

        self.stayOnScreen()

#*************************************************************************************************
#*************************************************************************************************
#changes the Player's velocity
    def change_velocity(self, velocity):
        self.velocity = velocity

#*************************************************************************************************
#*************************************************************************************************
#keeps the object in the screen
    def stayOnScreen(self):
        #left side of the screen
        if self.startPos.x <= 0:
            self.startPos.x = 0
            self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #right side of the screen
        elif self.startPos.x >= screen_width - self.height:
            self.startPos.x = screen_width - self.height
            self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #top of the screen
        if self.startPos.y <= 0:
            self.startPos.y = 0
            self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))

        #bottom of the screen
        elif self.startPos.y >= screen_height - self.height:
            self.startPos.y = 2 * (screen_height - self.height) - self.startPos.y
            if self.velocity.y > 0:
                self.velocity = euclid.Vector2(self.velocity.x, 0.0)
            #self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))

#*************************************************************************************************
#*************************************************************************************************
#returns the estamated last position of the object, could probably be improved/ not used for player
    def getLastPos(self, dtime):
        #self.lastPos = euclid.Vector2(self.startPos.x, self.startPos.y)
        startPos = euclid.Vector2(self.startPos.x, self.startPos.y)
        velocity = euclid.Vector2(self.velocity.x, self.velocity.y)
        startPos -= velocity * dtime

        velocity -= self.accel * dtime
        velocity.y += self.velocity.y * drag.y * dtime

        #self, startPos, height, length, screen=None, color=(255, 255, 255), accel = euclid.Vector2(0.0, 0.0), width=1)
        return SpritePlayer(startPos, self.height, self.length, self.screen, self.color, self.velocity, self.accel, self.width)

#*************************************************************************************************
#*************************************************************************************************
#returns a projectile that the Player shot
    def shoot(self, velocity=euclid.Vector2(400.0, 0.0), delay=.001, image=None):
        if delay >= BULLET_DELAY:
            return Projectile(euclid.Vector2(self.startPos.x + 1, self.startPos.y + 1), 15, 15, self.screen, BULLET_RANGE, image, velocity)
        return None

#*************************************************************************************************
#*************************************************************************************************
#returns the direction in radians that the object is movine in. 0 is to the right, pi & -pi are the left,
#down is negative
    def getDirection(self):
        return math.atan2(self.velocity.y, self.velocity.x)

#*************************************************************************************************
#*************************************************************************************************
#prints what I want to know
    def printPlayer(self):
        print "Player properties"
        print self.startPos
        print self.velocity
        print self.height
        print self.length
        print ""


#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
#****************************************************Platform*********************************************************************************************
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
class Platform(pygame.sprite.Sprite):

    def __init__(self, startPos, height, length, screen, image):
        pygame.sprite.Sprite.__init__(self)

        self.startPos = startPos
        self.length = length
        self.height = height
        self.screen = screen
        self.velocity = euclid.Vector2(0.0, 0.0)

        self.image = pygame.transform.scale(image, [int(length), int(height)])
        self.rect = self.image.get_rect()
        self.rect.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)

        #if screen is not None:  # if you can take out this and have it work that would be cool. i need it for reasons
            #self.display()

#*************************************************************************************************
#*************************************************************************************************
#shows the object
    def display(self):
        x1, y1 = int(self.startPos.x), int(self.startPos.y)
        self.rect = pygame.draw.rect(self.screen, self.color, (x1, y1, self.length, self.height))

#*************************************************************************************************
#*************************************************************************************************
#used to blit the image
    def update(self):
        self.screen.blit(self.image, (self.rect))
        self.rect.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)

#*************************************************************************************************
#*************************************************************************************************
#updates position and velocity
    def move(self, dtime):
        pass

#*************************************************************************************************
#*************************************************************************************************
#prints what I want to know
    def printPlatform(self):
        print "Plaftform properties"
        print self.startPos
        print self.height
        print self.length
        print ""


#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
#****************************************************Projectile*******************************************************************************************
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
class Projectile(pygame.sprite.Sprite):

    def __init__(self, startPos, height, length, screen=None, time=1, image=None, velocity=euclid.Vector2(0.0, 0.0), accel=euclid.Vector2(0.0, 0.0), width=0):
        pygame.sprite.Sprite.__init__(self)
        self.startPos = startPos
        self.velocity = velocity
        self.height = height
        self.length = length
        self.width = width
        self.accel = accel
        self.time = time
        self.screen = screen

        self.image = pygame.transform.scale(image, [int(length), int(height)])
        self.rect = self.image.get_rect()
        self.rect.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)
        #if screen is not None:  # if you can take out this if it would be cool. i need it for reasons
            #self.display()

#*************************************************************************************************
#*************************************************************************************************
#prints what I want to know
    def printProjectile(self):
        print "Projectile properties"
        print self.startPos
        print self.height
        print self.length
        print self.velocity
        print self.time
        print ""

#*************************************************************************************************
#*************************************************************************************************
#shows the object
    def display(self):
        rx, ry = int(self.startPos.x), int(self.startPos.y)
        self.rect = pygame.draw.rect(self.screen, self.color, (rx, ry, self.length, self.height))

#*************************************************************************************************
#*************************************************************************************************
#used to blit the image
    def update(self):
        self.screen.blit(self.image, (self.rect))
        self.rect.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)

#*************************************************************************************************
#*************************************************************************************************
#updates position and velocity
    def move(self, dtime):
        self.time -= dtime
        self.startPos += self.velocity * dtime
        self.velocity += self.accel * dtime
        #self.velocity.y -= self.velocity.y * drag.y * dtime
        self.stayOnScreen()

#*************************************************************************************************
#*************************************************************************************************
#returns the estamated last position of the object, could probably be improved
    def getLastPos(self, dtime):
        time = self.time
        time += dtime
        #self.lastPos = euclid.Vector2(self.startPos.x, self.startPos.y)
        startPos = euclid.Vector2(self.startPos.x, self.startPos.y)
        velocity = euclid.Vector2(self.velocity.x, self.velocity.y)
        startPos -= velocity * dtime

        try:  # man i don't know why i need this
            velocity -= self.accel * dtime
            velocity.y += self.velocity.y * drag.y * dtime
        except AssertionError:
            print "too bad"

        return Projectile(startPos, self.height, self.length, self.screen, time, self.image, velocity, self.accel, self.width)

#*************************************************************************************************
#*************************************************************************************************
#returns the direction in radians that the object is movine in. 0 is to the right, pi & -pi are the left,
#down is negative
    def getDirection(self):
        return math.atan2(self.velocity.y, self.velocity.x)

#*************************************************************************************************
#*************************************************************************************************
#keeps the object in the screen
    def stayOnScreen(self):
        #left side of the screen
        if self.startPos.x < 0:
            self.startPos.x = 0
            self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #right side of the screen
        elif self.startPos.x > screen_width - self.height:
            self.startPos.x = screen_width - self.height
            self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #top of the screen
        if self.startPos.y < 0:
            self.startPos.y = 0
            self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))

        #bottom of the screen
        elif self.startPos.y > screen_height - self.height:
            self.startPos.y = 2 * (screen_height - self.height) - self.startPos.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))


#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
#****************************************************Collisions*******************************************************************************************
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
class Collision:

    def __init__(self, dtime):
        self.dtime = dtime

#*************************************************************************************************
#*************************************************************************************************
#get the quadrant that the object is moveing in.
    def getQuadrant(self, direction):  # must call using projectile.getdirection()
        if direction <= 0 and direction > -math.pi / 2:
            #quadrant 1
            #print "1"
            return 1

        elif direction <= -math.pi / 2 and direction >= -math.pi:
            #quadrant 2
            #print "2"
            return 2

        elif direction > math.pi / 2 and direction <= math.pi:
            #quadrant 3
            #print "3"
            return 3

        elif direction <= math.pi / 2 and direction > 0:
            #quadrant 4
            #print "4"
            return 4

        return -1

#*************************************************************************************************
#*************************************************************************************************
#generates a larger rectangle to test for collisions with
    def getTestRectangle(self, A):
        quadrant = self.getQuadrant(A.getDirection())
        B = A.getLastPos(self.dtime)

        if quadrant % 2 == 1:
            if quadrant == 3:
                return Projectile(euclid.Vector2(A.startPos.x, B.startPos.y), ((A.startPos.y + A.height) - B.startPos.y), ((B.startPos.x + B.length) - A.startPos.x), A.screen, A.time, A.image)
            return Projectile(euclid.Vector2(B.startPos.x, A.startPos.y), ((B.startPos.y + B.height) - A.startPos.y), ((A.startPos.x + A.length) - B.startPos.x), A.screen, A.time, A.image)

        else:
            if quadrant == 4:
                return Projectile(euclid.Vector2(B.startPos.x, B.startPos.y), ((A.startPos.y + A.height) - B.startPos.y), ((A.startPos.x + A.length) - B.startPos.x), A.screen, A.time, A.image)
            return Projectile(euclid.Vector2(A.startPos.x, A.startPos.y), ((B.startPos.y + B.height) - A.startPos.y), ((B.startPos.x + B.length) - A.startPos.x), A.screen, A.time, A.image)

#*************************************************************************************************
#*************************************************************************************************
#detects collisions, this type of collision detectoin is used for projectiles.
    def detectCollision(self, projectile, rects):  # projectile is moving
        thingsHit = []
        lastProjectile = projectile.getLastPos(self.dtime)

        #if the current projectile and its last position are touching, then go ahead and use the
        #current projectile to test for collisions
        if pygame.sprite.collide_rect(projectile, lastProjectile):  # this if statement dosn't work and it's pissing me off. i don't see how it's wrong
            #testProjectile = projectile
            testProjectile = self.getTestRectangle(projectile)
        #if they are far apart from each other then make a different collision box
        else:
            testProjectile = self.getTestRectangle(projectile)

        for rect in rects:
            if pygame.sprite.collide_rect(testProjectile, rect):
                thingsHit.append(rect)

        if len(thingsHit) == 0:
            return NO_COLLISION

        #while there is a colision with the lastProjectile, get the last position of the projectile object
        #sometimes this happends and i dont know why. i would think it wouldn't be a problem but it is
        while pygame.sprite.collide_rect(lastProjectile, thingsHit[0]):
            lastProjectile = lastProjectile.getLastPos(self.dtime)

        #since the projectile must have hit somthing, change its current position to its last position
        #projectile.startPos = lastProjectile.startPos
        projectile.startPos = lastProjectile.startPos
        if len(thingsHit) >= 2:  # hit corner
            return HIT_CORNER

        elif len(thingsHit) == 1:
            quadrant = self.getQuadrant(projectile.getDirection())
            if quadrant == 1:
                #print "quad 1"
                if lastProjectile.startPos.y >= thingsHit[0].startPos.y + thingsHit[0].height:  # hit bottom
                    #projectile.startPos = euclid.Vector2(projectile.startPos.x, lastProjectile.startPos.y)
                    return HIT_BOTTOM
                else:  # hit right
                    #projectile.startPos = euclid.Vector2(lastProjectile.startPos.x, projectile.startPos.y)
                    return HIT_RIGHT

            elif quadrant == 2:
                #print "quad 2"
                if lastProjectile.startPos.y >= thingsHit[0].startPos.y + thingsHit[0].height:  # hit bottom
                    #projectile.startPos = euclid.Vector2(projectile.startPos.x, lastProjectile.startPos.y)
                    return HIT_BOTTOM
                else:  # hit left
                    #projectile.startPos = euclid.Vector2(lastProjectile.startPos.x, projectile.startPos.y)
                    return HIT_LEFT

            elif quadrant == 3:
                #print "quad 3"
                if lastProjectile.startPos.y - lastProjectile.height <= thingsHit[0].startPos.y:  # hit top
                    #projectile.startPos = euclid.Vector2(projectile.startPos.x, lastProjectile.startPos.y)
                    return HIT_TOP
                else:  # hit right
                    #projectile.startPos = euclid.Vector2(lastProjectile.startPos.x, projectile.startPos.y)
                    return HIT_RIGHT

            elif quadrant == 4:
                #print "quad 4"
                if lastProjectile.startPos.y - lastProjectile.height <= thingsHit[0].startPos.y:  # hit top
                    #projectile.startPos = euclid.Vector2(projectile.startPos.x, lastProjectile.startPos.y)
                    return HIT_TOP
                else:  # hit left
                    #projectile.startPos = euclid.Vector2(lastProjectile.startPos.x, projectile.startPos.y)
                    return HIT_LEFT

#*************************************************************************************************
#*************************************************************************************************
#detects collisions, this type of collision detectoin is used for players. this can be better
    def rectangleOnRectangle(self, rectA, rectB):  # rectA is the one that is moving

        if rectA.startPos.y <= rectB.startPos.y + rectB.height and rectA.startPos.y >= rectB.startPos.y + rectB.height - rectA.height / 2:
            if not (rectA.startPos.x + rectA.length < rectB.startPos.x or rectA.startPos.x > rectB.startPos.x + rectB.length):
                #print "botom"
                return HIT_BOTTOM

        elif rectA.startPos.y + rectA.height >= rectB.startPos.y and rectA.startPos.y + rectA.height <= rectB.startPos.y + rectA.height / 2:
            if not (rectA.startPos.x + rectA.length < rectB.startPos.x or rectA.startPos.x > rectB.startPos.x + rectB.length):
                #print "top"
                return HIT_TOP

        if rectA.startPos.x <= rectB.startPos.x + rectB.length and rectA.startPos.x >= rectB.startPos.x + rectB.length - rectA.length / 2:
            if not (rectA.startPos.y + rectA.height < rectB.startPos.y or rectA.startPos.y > rectB.startPos.y + rectB.height):
                #print "right"
                return HIT_RIGHT

        elif rectA.startPos.x + rectA.length >= rectB.startPos.x and rectA.startPos.x + rectA.length <= rectB.startPos.x + rectA.length / 2:
            if not (rectA.startPos.y + rectA.height < rectB.startPos.y or rectA.startPos.y > rectB.startPos.y + rectB.height):
                #print "left"
                return HIT_LEFT
        return NO_COLLISION


#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
#****************************************************Helper Methods***************************************************************************************
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
#*************************************************************************************************
#*************************************************************************************************
#resizes an image into a given surface
def resize(surface, size):
    scale = size / float(max(surface.get_rect().size))
    return pygame.transform.rotozoom(surface, 0, scale)