import sys
import os
import math
import random
import pygame
import pygame.mixer
import euclid
from pygame.locals import*

#class keystore:


def init(self):

    self.keyboard = {K_a: False}
    self.keyboard[K_b] = False
    self.keyboard[K_c] = False
    self.keyboard[K_d] = False
    self.keyboard[K_e] = False
    self.keyboard[K_f] = False
    self.keyboard[K_g] = False
    self.keyboard[K_h] = False
    self.keyboard[K_i] = False
    self.keyboard[K_j] = False
    self.keyboard[K_k] = False
    self.keyboard[K_l] = False
    self.keyboard[K_m] = False
    self.keyboard[K_n] = False
    self.keyboard[K_o] = False
    self.keyboard[K_p] = False
    self.keyboard[K_q] = False
    self.keyboard[K_r] = False
    self.keyboard[K_s] = False
    self.keyboard[K_t] = False
    self.keyboard[K_u] = False
    self.keyboard[K_v] = False
    self.keyboard[K_w] = False
    self.keyboard[K_x] = False
    self.keyboard[K_y] = False
    self.keyboard[K_z] = False
    self.keyboard[K_SPACE] = False

    self.left = 1
    self.middle = 2
    self.right = 3

    self.mouse = {self.left: False}
    self.mouse[self.middle] = False
    self.mouse[self.right] = False

    self.mposx = 0
    self.mposy = 0


def setPressed(self, events):

    for event in events:

        if event.type == pygame.QUIT:
            return False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return False

        elif event.type == MOUSEMOTION:
            self.mposx, self.mposy = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            for key in self.mouse.keys():
                if event.button == key:
                    self.mouse[key] = True
        elif event.type == MOUSEBUTTONUP:
            for key in self.mouse.keys():
                if event.button == key:
                    self.mouse[key] = False
        '''
        elif event.type == KEYDOWN:
            for key in self.keyboard.keys():
                if event.key == key:
                    self.keyboard[key] = True
        elif event.type == KEYUP:
            for key in self.keyboard.keys():
                if event.key == key:
                    self.keyboard[key] = False
        '''
    for key in self.keyboard.keys():
        keyboard[key] = pygame.key.get_pressed()[key]

    pygame.event.clear()
    pygame.event.pump()
    return True


def getVelocityToMouse(self, circle1, bulletSpeed=0):
    if self.mposx - circle1.startPos.x != 0:
        theta = math.atan((self.mposy - circle1.startPos.y) / (self.mposx - circle1.startPos.x))
        xcomp = bulletSpeed * math.cos(theta) * ((self.mposx - circle1.startPos.x) / math.fabs((self.mposx - circle1.startPos.x)))
        ycomp = bulletSpeed * math.sin(theta) * ((self.mposx - circle1.startPos.x) / math.fabs((self.mposx - circle1.startPos.x)))
    else:
        theta = ((self.mposy - circle1.startPos.y) / math.fabs((self.mposy - circle1.startPos.y)))
        xcomp = bulletSpeed * math.cos(theta)
        ycomp = bulletSpeed * math.sin(theta)
    return euclid.Vector2(xcomp, ycomp)


def getKeyValue(self, key):
    if key in keyboard.keys():
        return self.keyboard[key]
    else:
        return -1


def getMouseValue(self, key):
    if key in mouse.keys():
        return self.mouse[key]
    else:
        return -1