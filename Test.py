'''
Working on shooting circles. need to use a for loop to display all the projectiles
on the screen and also update their positions. after a preset tiem in the projectile
class, kill the object.

This is really a pretty cool program. Keep up the good work!
'''
import keystore
import sys
import os
import math
import random
import pygame
import pygame.mixer
import euclid

NO_COLLISION = 0
HIT_TOP = 1
HIT_BOTTOM = 2
HIT_RIGHT = 3
HIT_LEFT = 4

from pygame.locals import*

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

screen_size = screen_width, screen_height = 1000, 500
bulletSpeed = 250
BULLET_DELAY = .1
BULLET_RANGE = 10

initial_velocity = 80
drag = euclid.Vector2(50.0, 0.0)
gravity = euclid.Vector2(0.0, 500.0)
projectiles = []
platforms = []


#circle
class MyRectangle:

    def __init__(self, startPos, height, length, color=(255, 255, 255), accel = euclid.Vector2(0.0, 0.0), width=1):
        self.startPos = startPos
        self.velocity = euclid.Vector2(0, 0)
        self.height = height
        self.length = length
        self.color = color
        self.width = width
        self.accel = accel
        self.bitmap = pygame.image.load("saturn.gif")
        self.sprite = self.bitmap.get_rect()
        self.sprite.topleft = self.startPos
        self.right = True

    def render(self):
        screen.blit(pygame.transform.flip(self.bitmap, not self.right, 0), (self.sprite))
        self.sprite.center = euclid.Vector2(self.startPos.x + self.length / 2, self.startPos.y + self.height / 2)

    def display(self):
        rx, ry = int(self.startPos.x), int(self.startPos.y)
        self. rect = pygame.draw.rect(screen, self.color, (rx, ry, self.length, self.height), self.width)
        #self.render()

    def move(self, platforms=None):
        self.startPos += self.velocity * dtime + 0.5 * (self.accel * (dtime ** 2))
        self.velocity += self.accel * dtime
        self.velocity.x -= self.velocity.x * drag.x * dtime
        self.bounce(platforms)

    def change_velocity(self, velocity):
        self.velocity = velocity

    def printCircle(self):
        print self.color
        print self.velocity
        print self.startPos

    def bounce(self, platforms=None):

        for platform in platforms:
            if platform is not None:
                collision = rectangleOnRectangle(self, platform)
                if collision == NO_COLLISION:
                    collision = 0  # do nothing
                elif collision == HIT_TOP:
                    self.startPos.y = platform.startPos.y - self.height
                    self.velocity = euclid.Vector2(self.velocity.x, 0.0)
                elif collision == HIT_BOTTOM:
                    self.startPos.y = platform.startPos.y + platform.height
                    self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))
                elif collision == HIT_RIGHT:
                    self.startPos.x = platform.startPos.x + platform.length
                    self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))
                elif collision == HIT_LEFT:
                    self.startPos.x = platform.startPos.x - self.length
                    self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

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

    def shoot(self, velocity=euclid.Vector2(400.0, 0.0), delay=.001):
        if delay >= BULLET_DELAY:

            new_shot = Projectile(euclid.Vector2(self.startPos.x, self.startPos.y), BULLET_RANGE, blue, velocity)
            '''
            if self.right:
                new_shot = Projectile(euclid.Vector2(self.startPos.x + self.length, self.startPos.y + self.height / 2), BULLET_RANGE, blue, velocity)
            else:
                new_shot = Projectile(euclid.Vector2(self.startPos.x, self.startPos.y + self.height / 2), BULLET_RANGE, blue, velocity)
                '''
            projectiles.append(new_shot)
            return True
        return False

class Platform:

    def __init__(self, startPos, height, length, color=(255, 255, 255)):
        self.startPos = startPos
        self.length = length
        self.height = height
        self.color = color

    def display(self):
        x1, y1 = int(self.startPos.x), int(self.startPos.y)
        self.rect = pygame.draw.rect(screen, self.color, (x1, y1, self.length, self.height))



class Projectile:

    def __init__(self, position, time, color=(255, 255, 255), velocity = euclid.Vector2(0.0, 0.0), accel = euclid.Vector2(0.0, 0.0), width=0):
        self.position = position
        self.velocity = velocity
        self.size = 5
        self.color = color
        self.width = width
        self.accel = accel
        self.time = time

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.color, (rx, ry), self.size, self.width)

    def move(self, platforms=None):
        self.position += self.velocity * dtime
        self.velocity += self.accel * dtime
        self.bounce(platforms)
        self.velocity.y -= self.velocity.y * drag.y * dtime
        #update time so you know when to kill the bullet
        self.time -= dtime

    def bounce(self, platforms=None):
        for platform in platforms:
            if platform is not None:
                #bottom of plat

                if self.position.y - self.size <= platform.startPos.y + platform.height and self.position.y - self.size >= platform.startPos.y - self.size:
                    if not (self.position.x < platform.startPos.x or self.position.x > platform.startPos.x + platform.length):
                        self.position.y = platform.startPos.y + platform.height + self.size
                        self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))

                #top of plat
                elif self.position.y + self.size >= platform.startPos.y and self.position.y + self.size <= platform.startPos.y + self.size:
                    if not (self.position.x < platform.startPos.x or self.position.x > platform.startPos.x + platform.length):
                        self.position.y = platform.startPos.y - self.size
                        self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))

                #left side of plat
                if self.position.x - self.size <= platform.startPos.x + platform.length and self.position.x - self.size >= platform.startPos.x - self.size:
                    if not (self.position.y < platform.startPos.y or self.position.y > platform.startPos.y + platform.height):
                        self.position.x = platform.startPos.x + platform.length + self.size
                        self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

                #right side of plat
                elif self.position.x + self.size >= platform.startPos.x and self.position.x + self.size <= platform.startPos.x + self.size:
                    if not (self.position.y < platform.startPos.y or self.position.y > platform.startPos.y + platform.height):
                        self.position.x = platform.startPos.x - self.size
                        self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #left side of the screen
        if self.position.x <= self.size:
            self.position.x = 2 * self.size - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #right side of the screen
        elif self.position.x >= screen_width - self.size:
            self.position.x = 2 * (screen_width - self.size) - self.position.x
            self.velocity = self.velocity.reflect(euclid.Vector2(1, 0))

        #top of the screen
        if self.position.y <= self.size:
            self.position.y = 2 * self.size - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))

        #bottom of the screen
        elif self.position.y >= screen_height - self.size:
            self.position.y = 2 * (screen_height - self.size) - self.position.y
            self.velocity = self.velocity.reflect(euclid.Vector2(0, 1))


def rectangleOnRectangle(rectA, rectB):  # rectA is the one that is moving

    if rectA.startPos.y <= rectB.startPos.y + rectB.height and rectA.startPos.y >= rectB.startPos.y + rectB.height - rectA.height / 2:
        if not (rectA.startPos.x + rectA.length < rectB.startPos.x or rectA.startPos.x > rectB.startPos.x + rectB.length):
            print "botom"
            return HIT_BOTTOM

    elif rectA.startPos.y + rectA.height >= rectB.startPos.y and rectA.startPos.y + rectA.height <= rectB.startPos.y + rectA.height / 2:
        if not (rectA.startPos.x + rectA.length < rectB.startPos.x or rectA.startPos.x > rectB.startPos.x + rectB.length):
            print "top"
            return HIT_TOP

    if rectA.startPos.x <= rectB.startPos.x + rectB.length and rectA.startPos.x >= rectB.startPos.x + rectB.length - rectA.length / 2:
        if not (rectA.startPos.y + rectA.height < rectB.startPos.y or rectA.startPos.y > rectB.startPos.y + rectB.height):
            print "right"
            return HIT_RIGHT

    elif rectA.startPos.x + rectA.length >= rectB.startPos.x and rectA.startPos.x + rectA.length <= rectB.startPos.x + rectA.length / 2:
        if not (rectA.startPos.y + rectA.height < rectB.startPos.y or rectA.startPos.y > rectB.startPos.y + rectB.height):
            print "left"
            return HIT_LEFT
    return NO_COLLISION


screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

pygame.display.set_caption("First Class!")


#make circle *****************************
height = 40
length = 40
x = screen_width / 2
y = screen_height - height

circle1 = MyRectangle(euclid.Vector2(x, y), height, length, red, gravity, 0)
#******************************************

# startPos, endPos, length, color=(255, 255, 255))
platform1 = Platform(euclid.Vector2(200, 300), 10, 400, black)
platforms.append(platform1)
platform2 = Platform(euclid.Vector2(0, 200), 10, 400, black)
platforms.append(platform2)
platform3 = Platform(euclid.Vector2(0, 100), 10, 400, black)
platforms.append(platform3)
platform4 = Platform(euclid.Vector2(400, 400), 10, 400, black)
platforms.append(platform4)

platform5 = Platform(euclid.Vector2(700, 0), 400, 100, black)
platforms.append(platform5)
platform6 = Platform(euclid.Vector2(900, 0), 400, 100, black)
platforms.append(platform6)
platform7 = Platform(euclid.Vector2(0, screen_height / 2), 400, 100, black)
platforms.append(platform7)


fps_limit = 60
run_me = True
keystore.init(keystore)
timeSinceLastShot = 0

while run_me:
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms / 1000.0

    events = pygame.event.get()
    run_me = keystore.setPressed(keystore, events)
    bulletVec = keystore.getVelocityToMouse(keystore, circle1, bulletSpeed)
    if keystore.getMouseValue(keystore, keystore.left):
        if circle1.shoot(bulletVec, timeSinceLastShot):
            timeSinceLastShot = 0
    timeSinceLastShot += dtime

    if keystore.getKeyValue(keystore, K_a):
        circle1.right = False
        circle1.change_velocity(euclid.Vector2(-500.0, circle1.velocity.y))
    if keystore.getKeyValue(keystore, K_d):
        circle1.right = True
        circle1.change_velocity(euclid.Vector2(500.0, circle1.velocity.y))
    if keystore.getKeyValue(keystore, K_w):
        if circle1.velocity.y == 0:
            circle1.change_velocity(euclid.Vector2(circle1.velocity.x, -400.0))
    #if keystore.getKeyValue(keystore, K_s):
        #print "do nothing"
        #do nothing for now

    #Clear the screen
    #screen.lock()
    screen.fill(white)

    #projectile stuff
    for projectile in projectiles:
        if projectile.time <= 0:
            projectiles.remove(projectile)
        else:
            projectile.display()
            projectile.move(platforms)

    #circle stuff
    circle1.move(platforms)
    circle1.display()

    #platform stuff
    for platform in platforms:
        platform.display()

    #screen.unlock()

    #display everything in the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
