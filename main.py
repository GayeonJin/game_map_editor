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

TITLE_STR = "Game Editor"

INFO_HEIGHT = 40
INFO_OFFSET = 10
INFO_FONT = 20

def draw_message(str) :
    font = pygame.font.Font('Verdana', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))

    gctrl.gamepad.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def draw_info() :
    font = pygame.font.SysFont('Verdana', INFO_FONT)
    info = font.render('F1 : load map   F2 : save map   F10 : capture scr   1-7 : item  space : select', True, COLOR_BLACK)

    pygame.draw.rect(gctrl.gamepad, COLOR_PURPLE, (0, gctrl.pad_height - INFO_HEIGHT, gctrl.pad_width, INFO_HEIGHT))
    gctrl.gamepad.blit(info, (INFO_OFFSET * 2, gctrl.pad_height - INFO_FONT - INFO_OFFSET))

def terminate() :
    pygame.quit()
    sys.exit()

def edit_map() :
    global clock
    global map, res_ctrl

    cursor = cursor_object(map)
    cursor.x = 0
    cursor.y = 0

    direction = 0
    
    pre_x = 0
    pre_y = 0
    mouse_drag = False

    map_type = 0
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = CURSOR_MOVE_DOWN
                elif event.key == pygame.K_DOWN :
                    direction = CURSOR_MOVE_UP
                elif event.key == pygame.K_LEFT :
                    direction = CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = CURSOR_MOVE_RIGHT
                elif event.key >= pygame.K_1 and event.key <= pygame.K_7 : 
                    map_type = event.key - pygame.K_0
                elif event.key == pygame.K_SPACE :
                    map_type = res_ctrl.get_select()
                elif event.key == pygame.K_F1 :               
                    map.load()
                elif event.key == pygame.K_F2 :
                    map.save()
                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN :
                l_button, wheel, r_button = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                x, y = map.get_pos(mouse_pos)
                if x != None or y != None :
                    mouse_drag = True
                    cursor.set_pos(x, y)
                    if l_button :
                        map.set_map_type(cursor.x, cursor.y, res_ctrl.get_select())
                    pre_x = x
                    pre_y = y

            elif event.type == pygame.MOUSEMOTION :
                if mouse_drag == True :
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = map.get_pos(mouse_pos)
                    if x != None or y != None :
                        if pre_x != x or pre_y != y :
                            cursor.set_pos(x, y)
                            if l_button :
                                map.set_map_type(cursor.x, cursor.y, res_ctrl.get_select())          
                            pre_x = x
                            pre_y = y

            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_drag = False
                mouse_pos = pygame.mouse.get_pos()
                x, y = map.get_pos(mouse_pos)
                if x != None or y != None :
                    if pre_x != x or pre_y != y :
                        cursor.set_pos(x, y)
                        if l_button :
                            map.set_map_type(cursor.x, cursor.y, res_ctrl.get_select())
                        pre_x = x
                        pre_y = y

                x, y = res_ctrl.get_pos(mouse_pos)
                if x != None and y != None :
                    res_ctrl.select(x, y)                        

        # Move cursor
        if direction != 0 :
            cursor.move(direction)
            direction = 0

        # Change wall
        if map_type != 0 :
            map.set_map_type(cursor.x, cursor.y, map_type)
            map_type = 0
            
        # Clear gamepad
        gctrl.gamepad.fill(COLOR_WHITE)

        # Draw map
        map.draw()

        # Draw cursor
        cursor.draw_rect(COLOR_BLACK, 1)

        # Draw resource control
        res_ctrl.draw()

        # Draw info
        draw_info()

        pygame.display.update()
        clock.tick(60)

def start_game_edit() :
    # Clear gamepad
    gctrl.gamepad.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render(TITLE_STR, True, COLOR_BLACK)
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
    global map, res_ctrl

    pygame.init()
    clock = pygame.time.Clock()

    # register resource
    m_res = map_resource()
    for i, resource_key in enumerate(resource_map_item) :
        m_res.add(resource_key, game_object(0, 0, get_map_resource(resource_key)))

    # map
    map = game_map(MAX_ROWS, MAX_COLS)
    map.register_resouce(m_res)
    map_rect = map.get_pad_rect()

    # resource control
    res_ctrl = resource_map(1, m_res.get_length(), MAP_XOFFSET, MAP_YOFFSET + map_rect.bottom)
    res_ctrl.register_resouce(m_res)
    res_ctrl_rect = res_ctrl.get_pad_rect()

    for i in range(m_res.get_length()) :
        res_ctrl.set_map_type(i, 0, i + 1)

    pad_width = map_rect.width
    pad_height = res_ctrl_rect.bottom + INFO_HEIGHT

    gctrl.set_param(pygame.display.set_mode((pad_width, pad_height)), pad_width, pad_height)
    pygame.display.set_caption(TITLE_STR)

if __name__ == '__main__' :
    init_game_edit()
    while True :
        mode = start_game_edit()
        if mode == 'edit' :
            edit_map()
        elif mode == 'test' :
            print('not yet')

