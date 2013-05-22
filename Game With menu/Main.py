'''
Developed by Matt Bauer
**Make your mark

Last update: 5, 22, 2013



Notes:

        Need to install pygame in additon to python.
        Need the keystore file and the euclid file in the same directory as Test.py
        Performs best with bulletSpeed of 500 or less

Images:
        bgmenue2small.png
        fireball.png
        platform.jpg
        spaceman.pgn

Known problems:

        When the player shoots at a wall that is thin and touches the edje of the screen,
        if the bullet is traveling VERY fast, the program will go into an infinit loop.  The loop
        occers in the detectCollision() method in the while loop.  (the green platform at top will cause
        loop, but the left and right sides will not)

        Since the player can jump when it's Y velocity is 0, they can somtimes jump at the apex of the
        last jump.  Easy to fix, just haven't yet

        Bullets are getting stuck when hitting the very corner of a platform at a 45 ish degree angle.
        I think it's only a problem when shooting from quadrant 1

        When the player shoots at the corner of a platform that is also toucching the screen, it will
        not change the velocity of the bullet and it will become stuck in the corner

        Since this program is calculating the collisions for the player differently than the bullets,
        the player will somtimes travel through a platform when the game drops frames.  This can be fixed
        by using the same collision detecction as the bullets i think.

        When the user moves the game window shit goes crazy and things might get stuck.

        Somthing's fucked up with detectCollisions method in Main. if we get it working we can shoot
        shit going at any speed, but untill then, try to keep that shit under 700 pps

        Problem when collisioncode is 5 aka when projectile hits a corner


Usefull Shit:

        http://tech.pro/tutorial/1007/collision-detection-with-pygame
            tells how to make sureface for sprites
'''
import keystore
import sys
import os
import math
import random
import pygame
import pygame.mixer
import euclid

from mainMenu import*
from gameClasses import*
from pygame.locals import*

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

screen_size = screen_width, screen_height = 1000, 500
bulletImage = pygame.image.load("fireball.png")
wallImage = pygame.image.load("platform.jpg")
gameBG = pygame.transform.scale(pygame.image.load("gameBG.jpg"), [screen_width, screen_height])
fps_limit = 60
bulletSpeed = 800

initial_velocity = 80
#drag = euclid.Vector2(50.0, 0.0)
gravity = euclid.Vector2(0.0, 1500.0)
projectiles = []
platforms = []
sprites = pygame.sprite.RenderPlain()


def richochet(bullet, collisionCode):

        if collisionCode == NO_COLLISION:
            return

        if collisionCode == HIT_BOTTOM:
            bullet.velocity = bullet.velocity.reflect(euclid.Vector2(0, 1))

        if collisionCode == HIT_TOP:
            bullet.velocity = bullet.velocity.reflect(euclid.Vector2(0, 1))

        if collisionCode == HIT_RIGHT:
            bullet.velocity = bullet.velocity.reflect(euclid.Vector2(1, 0))

        if collisionCode == HIT_LEFT:
            bullet.velocity = bullet.velocity.reflect(euclid.Vector2(1, 0))

        if collisionCode == HIT_CORNER:
            bullet.velocity = euclid.Vector2(-bullet.velocity.x, -bullet.velocity.y)


def walk(player, collisionCode):

        if collisionCode == NO_COLLISION:
            pass
        elif collisionCode == HIT_TOP:
            player.startPos.y = platform.startPos.y - player.height
            player.velocity = euclid.Vector2(player.velocity.x, 0.0)
        elif collisionCode == HIT_BOTTOM:
            player.startPos.y = platform.startPos.y + platform.height
            player.velocity = player.velocity.reflect(euclid.Vector2(0, 1))
        elif collisionCode == HIT_RIGHT:
            player.startPos.x = platform.startPos.x + platform.length
            player.velocity = player.velocity.reflect(euclid.Vector2(1, 0))
        elif collisionCode == HIT_LEFT:
            player.startPos.x = platform.startPos.x - player.length
            player.velocity = player.velocity.reflect(euclid.Vector2(1, 0))

#***********************************************************************************************************
#*****************************************Main**************************************************************
#run main menu...
menu = App()

screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

pygame.display.set_caption("First Class!")

bigHardOnCollider = Collision(0.0)

#make player *****************************
height = 30
length = 20
x = screen_width / 2
y = screen_height - height

player1 = SpritePlayer(euclid.Vector2(x, y), height, length, screen, euclid.Vector2(0.0, 0.0), gravity, 0)

sprites.add(player1)
#******************************************

# startPos, endPos, length, color=(255, 255, 255))
platform1 = Platform(euclid.Vector2(200, 300), 10, 400, screen, wallImage)
platforms.append(platform1)
platform2 = Platform(euclid.Vector2(0, 200), 10, 400, screen, wallImage)
platforms.append(platform2)
platform3 = Platform(euclid.Vector2(0, 100), 10, 400, screen, wallImage)
platforms.append(platform3)
platform4 = Platform(euclid.Vector2(400, 400), 10, 400, screen, wallImage)
platforms.append(platform4)

platform5 = Platform(euclid.Vector2(800, 0), 150, 10, screen, wallImage)
platforms.append(platform5)
platform5 = Platform(euclid.Vector2(800, 200), 150, 10, screen, wallImage)
platforms.append(platform5)
platform6 = Platform(euclid.Vector2(900, 0), 400, 10, screen, wallImage)
platforms.append(platform6)
platform7 = Platform(euclid.Vector2(0, screen_height / 2), 400, 100, screen, wallImage)
platforms.append(platform7)
platform8 = Platform(euclid.Vector2(600, 200), 10, 300, screen, wallImage)
platforms.append(platform8)
#platform9 = Platform(euclid.Vector2(0, 0), 10, screen_width, screen, wallImage)
#platforms.append(platform9)
#platform10 = Platform(euclid.Vector2(0, 0), screen_height, 10, screen, wallImage)
#platforms.append(platform10)



run_me = True
keystore.init(keystore)
timeSinceLastShot = 0  # think about adding this as a Player or gun attribute

while run_me:
    #dtime_ms = clock.tick(fps_limit)
    bigHardOnCollider.dtime = clock.tick(fps_limit) / 1000.0

    events = pygame.event.get()
    run_me = keystore.setPressed(keystore, events)
    bulletVec = keystore.getVelocityToMouse(keystore, player1, bulletSpeed)
    if keystore.getMouseValue(keystore, keystore.left):
        shot = player1.shoot(bulletVec, timeSinceLastShot, bulletImage)
        if shot is not None:
            projectiles.append(shot)
            #sprites.add(shot)
            timeSinceLastShot = 0
    timeSinceLastShot += bigHardOnCollider.dtime

    if keystore.getKeyValue(keystore, K_a):
        player1.right = False
        player1.change_velocity(euclid.Vector2(-300.0, player1.velocity.y))
    if keystore.getKeyValue(keystore, K_d):
        player1.right = True
        player1.change_velocity(euclid.Vector2(300.0, player1.velocity.y))
        #problem with jumping.  Change to after collide reset jump
    if keystore.getKeyValue(keystore, K_w):
        if player1.velocity.y == 0:
            player1.change_velocity(euclid.Vector2(player1.velocity.x, -600.0))
    #if keystore.getKeyValue(keystore, K_s):
        #print "do nothing"
        #do nothing for now

    #Clear the screen
    #screen.lock()
    #screen.fill(gameBG)
    screen.blit(gameBG, (0, 0))

    #platforms.append(player1)

    #projectile stuff
    for projectile in projectiles:
        if projectile.time <= 0:
            projectiles.remove(projectile)
            #gc.collect()
        else:
            projectile.move(bigHardOnCollider.dtime)
            richochet(projectile, bigHardOnCollider.detectCollision(projectile, platforms))  # collision class?
            projectile.update()

    #platforms.remove(player1)

    #Player stuff
    player1.move(bigHardOnCollider.dtime)
    #sprites.draw(screen)
    #platform stuff
    for platform in platforms:
        walk(player1, bigHardOnCollider.rectangleOnRectangle(player1, platform))  # collision class?
        platform.update()
    player1.update()

    #screen.unlock()

    #display everything in the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
