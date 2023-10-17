#!/usr/bin/python

import os
import sys
import csv

import pygame
import random
from time import sleep

from tkinter import filedialog
from tkinter import *

from gresource import *
from gobject import *

from map import *
from cursor import *

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))

    gctrl.gamepad.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def edit_map() :
    global clock
    global map

    cursor = cursor_object(map)

    cursor.x = 0
    cursor.y = 0
    direction = 0
    
    map_type = 0
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = CURSOR_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    direction = CURSOR_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    direction = CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = CURSOR_MOVE_RIGHT
                elif event.key == pygame.K_1 :
                    map_type = 1
                elif event.key == pygame.K_2 :
                    map_type = 2
                elif event.key == pygame.K_3 :
                    map_type = 3
                elif event.key == pygame.K_4:
                    map_type = 4
                elif event.key == pygame.K_5 :
                    map_type = 5
                elif event.key == pygame.K_6 :
                    map_type = 6
                elif event.key == pygame.K_7:
                    map_type = 7        
                elif event.key == pygame.K_q :               
                    map.load()
                elif event.key == pygame.K_w :
                    map.save()
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos()
                x, y = map.get_pos(mouse_pos)
                if x != None or y != None :
                    cursor.set_pos(x, y)               

        # Move cursor
        if direction != 0 :
            cursor.move(direction)
            direction = 0

        # Change wall
        if map_type != 0 :
            map.edit_map(cursor.x, cursor.y, map_type)
            map_type = 0
            
        # Clear gamepad
        gctrl.gamepad.fill(COLOR_WHITE)

        # Draw map
        map.draw()

        # Draw cursor
        cursor.draw_rect(COLOR_BLACK, 1)

        pygame.display.update()
        clock.tick(60)

def start_game_edit() :
    # Clear gamepad
    gctrl.gamepad.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render("Game Editor", True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))
    gctrl.gamepad.blit(text_suf, text_rect)

    help_str = ['e : edit map',
                't : test map',
                'x : exit']

    font1 = pygame.font.SysFont(None, 25)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.pad_width / 2
        gctrl.gamepad.blit(text_suf1, text_rect1)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_e :
                    return 'edit'
                elif event.key == pygame.K_t :
                    return 'test'
                elif event.key == pygame.K_x :
                    terminate()

        pygame.display.update()
        clock.tick(60)    
       
def init_game_edit() :
    global clock
    global map

    pygame.init()
    clock = pygame.time.Clock()

    # map
    map = map_object(MAX_ROWS, MAX_COLS)
    for i, resource_key in enumerate(resource_map_item) :
        map.add_objet(resource_key, game_object(0, 0, get_map_resource(resource_key)))

    (pad_width, pad_height) = map.get_padsize()

    gctrl.set_param(pygame.display.set_mode((pad_width, pad_height)), pad_width, pad_height)
    pygame.display.set_caption("Game Editor")

if __name__ == '__main__' :
    init_game_edit()
    while True :
        mode = start_game_edit()
        if mode == 'edit' :
            edit_map()
        elif mode == 'test' :
            print('not yet')

