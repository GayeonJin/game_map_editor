#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *

class game_object :
    def __init__(self, x, y, resource_path) :
        if resource_path != None :
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width()
            self.height = self.object.get_height()
        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.set_position(x, y)

        self.life_count = 1

    def set_position(self, x, y) : 
        self.x = x
        self.y = y
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def move(self, del_x, del_y) :
        self.x += del_x
        self.y += del_y

        if self.y < 0 :
            self.y = 0
        elif self.y > (gctrl.height - self.height) :
            self.y = (gctrl.height - self.height)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self, rect) :
        if self.object != None :
            gctrl.surface.blit(self.object, rect)

gctrl = game_ctrl()

if __name__ == '__main__' :
    print('game control and object')