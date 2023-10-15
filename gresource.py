#!/usr/bin/python

import sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

resource_path = ''

resource_img_item = {
    'id_background' : 'image/background.png',
}

resource_map_item = {
    'id_block_plain' : 'image/Plain_Block.png',
    'id_block_grass' : 'image/Grass_Block.png',
    'id_block_wall_tall' : 'image/Wall_Block_Tall.png',
    'id_block_wood_tall' : 'image/Wood_Block_Tall.png',  
    'id_tree_short' : 'image/Tree_Short.png',
    'id_tree_tall' : 'image/Tree_Tall.png',
    'id_tree_ugly' : 'image/Tree_Ugly.png',
}

def get_img_resource(resource_id) :
    return resource_path + resource_img_item[resource_id]

def get_map_resource(resource_id) : 
    return resource_path + resource_map_item[resource_id]

if __name__ == '__main__' :
    print('game resoure')