#!/usr/bin/python

import sys
import csv

import pygame
import random

from gresource import *
from gobject import *

MAX_ROWS = 8
MAX_COLS = 16

MAP_XOFFSET = 10
MAP_YOFFSET = 50

MAP_WIDTH = 30
MAP_HEIGHT = 30

map_dict = {
    1 : ['id_block_plain'],
    2 : ['id_block_grass'],
    3 : ['id_block_wall_tall'],
    4 : ['id_block_wood_tall'],  
    5 : ['id_block_grass', 'id_tree_short'],
    6 : ['id_block_grass', 'id_tree_tall'],
    7 : ['id_block_grass', 'id_tree_ugly'],    
}

class map_resource :
    def __init__(self, width = MAP_WIDTH , height = MAP_HEIGHT) :
        self.object = {}
        self.width = width
        self.height = height

    def add(self, key, item) :
        self.object[key] = item
        self.width = item.width
        self.height = item.height

    def draw(self, map_type, rect) :
        keys = map_dict[map_type]
        if keys != None :
            for key in keys :
                self.object[key].draw(rect)

            return True
        return False        

class map_object :
    def __init__(self, rows, cols) :
        self.map = []

        self.rows = rows
        self.cols = cols
        
        for x in range(cols) :
            self.map.append([])
            for y in range(rows) :
                self.map[x].append(1)

        self.x_offset = MAP_XOFFSET
        self.y_offset = MAP_YOFFSET

    def register_resouce(self, resource) :
        self.resource = resource
        self.pad_width = 2 * self.x_offset + self.cols * self.resource.width
        self.pad_height = 2 * self.y_offset + self.rows * self.resource.height

    def get_size(self) :
        return self.rows, self.cols

    def get_padsize(self) :
        return (self.pad_width, self.pad_height) 

    def get_pos(self, screen_xy) :
        for y in range(self.rows) :
            for x in range(self.cols) :
                map_rect = self.get_map_rect(x, y)
                if screen_xy[0] > map_rect.left and screen_xy[0] < map_rect.right :
                    if screen_xy[1] > map_rect.top and screen_xy[1] < map_rect.bottom :      
                        return (x, y)
                    
        return (None, None)

    def get_map_rect(self, x, y) :
        width = self.resource.width
        height = self.resource.height
        map_rect = pygame.Rect(self.x_offset, self.y_offset, width, height)

        # map[0][0] is left and bottom
        map_rect.x += x * width 
        map_rect.y += ((self.rows - 1) - y) * height
        return map_rect        

    def get_map_type(self, x, y) :
        return self.map[x][y]

    def draw(self) :
        map_rect = self.get_map_rect(0, 0)

        for y in range(self.rows) :
            for x in range(self.cols) :
                if self.resource.draw(self.map[x][y], map_rect) == False :
                    pygame.draw.rect(gctrl.gamepad, COLOR_RED, map_rect, 1, 1)

                map_rect.x += map_rect.width
            map_rect.y -= map_rect.height
            map_rect.x = self.x_offset

    def load(self, filename = 'default_map.csv') :
        print("load map : " + filename)

        file = open(filename, 'r')
        rows = csv.reader(file)

        x = 0
        y = 0
        for row in rows :
            for value in row :
                self.map[x][y] = int(value)
                x += 1
            y += 1
            x = 0

        print(self.map)

    def save(self, filename = 'default_map.csv') :
        print("save map : " + filename)

        with open(filename, 'w') as file:
            #for header in header:
            #    file.write(str(header)+', ')
            #file.write('n')
            for y in range(self.rows):
                for x in range(self.cols - 1):
                    file.write(str(self.map[x][y])+', ')
                file.write(str(self.map[x+1][y]))
                file.write('\n')

    def edit_map(self, x, y, map_type) :
        if map_type != None :
            self.map[x][y] = map_type 

if __name__ == '__main__' :
    print('game map resource and object')
