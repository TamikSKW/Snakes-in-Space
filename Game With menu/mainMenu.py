#!/usr/bin/env python
#-*- coding: utf-8 -*-

# TJ Brosnan
# MainMenu needs all resources in same path as itself for now:
# zebulon.ttf and bgmenu2small.png
# The png has a gradient transparency in the middle to make the menu look like
#     it fades away.

import sys
import pygame
from pygame.locals import *



class App:

    def __init__(self):
        self.screen = [800, 600]
        screenX = 800
        screenY = 600
        self.white = [255, 255, 255]
        self.background = pygame.image.load("bgmenu2small.png")
        self.menu = [" Start ", " Options ", " Exit "]
        self.menuall = ""
        self.selectedmenu = 0
        self.mid = []
        # set pygame options
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen, 0, 32)
        pygame.display.set_caption("BMenu")
        # get menu width
        self.menuid()
        # all menu in one:
        self.listmenuall()

        startGame = False
        # mainloop
        while not startGame:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_LEFT:
                        if self.selectedmenu == 0:
                            self.selectedmenu = len(self.menu) - 1
                        else:
                            self.selectedmenu = self.selectedmenu - 1
                    elif self.event.key == pygame.K_RIGHT:
                        if self.selectedmenu == len(self.menu) - 1:
                            self.selectedmenu = 0
                        else:
                            self.selectedmenu = self.selectedmenu + 1
                    elif self.event.key == pygame.K_RETURN:
                        if self.selectedmenu == len(self.menu) - 3:  # start pressed
                            startGame = True
                        if self.selectedmenu == len(self.menu) - 2:  # options pressed
                            pass
                        if self.selectedmenu == len(self.menu) - 1:  # exit pressed
                            pygame.quit()
                            sys.exit()
            # getFinalPos if there was just a button pressed
            # getScrollDir if there was just a button pressed
            # getscrolldir will also set the x velocity
            # move dat menu
            # 2nd layer: menus
            self.crt_menu()
            # 3rd layer: transparent image
            self.screen.blit(self.background, (0, 0))
            # 4th layer: title
            self.crt_title()
            pygame.display.flip()

    def menuid(self):
        for n in self.menu:
            font = pygame.font.SysFont("arial", 40)
            text_surface = font.render(n, True, self.white)
            self.mid.append(text_surface.get_width())

    def listmenuall(self):
        for n in self.menu:
            self.menuall = self.menuall + n

    def crt_menu(self):
        nmb = 0
        xpos = 0
        velocityx = 0
        finalxpos = 0
        scrollspeed = 30
        #getfinalpos
        while nmb <= self.selectedmenu:
            finalxpos = finalxpos - self.mid[nmb]
            xpos = finalxpos
            nmb = nmb + 1
        finalxpos = finalxpos + self.mid[self.selectedmenu] / 2

        # draw menus on screen
        font = pygame.font.SysFont("arial", 40)
        text_surface = font.render(self.menuall, True, self.white)
        #TODO: change this after testing
        self.screen.blit(text_surface, (400 + finalxpos, 280))

    def crt_title(self):
        title = pygame.font.Font("Zebulon.ttf", 70)
        textTitle_surface = title.render("Space Snakes", True, self.white)
        self.screen.blit(textTitle_surface, (20, 140))

#if __name__ == "__main__":
    #App()