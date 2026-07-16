import numpy as np
import math
import pygame as pg
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#--------------------------------#
from engine.configs.configs import configs
from engine.raycaster3D.sprites import SpriteManager
from engine.raycaster3D.doors import DoorManager
from engine.utils.dict_to_class import dict_to_class
from engine.utils.overlay import debug_overlay
#--------------------------------#
from engine.raycaster3D.constants import worldMap, default_thin_walls_data, default_doors, default_sprites_list
#--------------------------------#
from engine.raycaster3D.renderer.renderer_sprites import render_sprites
from engine.raycaster3D.renderer.walls_renderer import render_walls
from engine.raycaster3D.renderer.floor_ceiling_render import render_floor_ceiling
#================================#
type array =  np.array
type array_surf =  np.array
type surface =  pg.Surface
#================================#
class RaycasterRenderer:
    #--------------------------------#
    def __init__(self):
        self.buffer = np.zeros((configs.game.raysurface_size[1], configs.game.raysurface_size[0]), dtype=np.uint32)  # screen buffer
        self.ZBuffer = np.zeros(configs.game.raysurface_size[0], dtype=np.float64)   # walls distance
        #--------------------------------#
        self.sprite_manager = SpriteManager(
            default_sprites_list
        )
        self.door_manager = DoorManager(
            default_doors
        )
        #--------------------------------#
        globalclasses.SpriteManager = self.sprite_manager
        globalclasses.DoorManager = self.door_manager
        #--------------------------------#
        self.thin_walls = default_thin_walls_data
        self.grid = worldMap
        self.ceil_grid = worldMap
        self.floor_grid = worldMap
        self.floorDefaultTex1 = 56
        self.floorDefaultTex2 = 57
        self.ceilDefaultTex = 58
    #--------------------------------#
    def render(self, textures:array_surf, pos, dir, plane):
        #--------------------------------#
        TEX_W = configs.game.raytexture_size      
        TEX_H = configs.game.raytexture_size   
        #---------cleans buff---------#
        self.buffer[:] = 0
        self.ZBuffer[:] = 1e30  # infinito'
        #---------floor and ceiling render---------#camera:object, world:object, textures:array_surf, sprites:array
        render_floor_ceiling(
            pos.x, pos.y,
            dir.x, dir.y,
            plane.x, plane.y,
            textures, 
            self.buffer,
            self.ZBuffer,
            self.ceil_grid, self.floor_grid,
            floorDefaultTex1 = self.floorDefaultTex1, floorDefaultTex2 = self.floorDefaultTex2, ceilDefaultTex = self.ceilDefaultTex,
            TEX_W=TEX_W,TEX_H=TEX_H

        )
        #---------walls render---------#
        render_walls(
            pos.x, pos.y,
            dir.x, dir.y,
            plane.x, plane.y,
            self.grid,
            textures,
            self.buffer,
            self.ZBuffer,
            self.thin_walls,
            self.door_manager.get_array(),
            TEX_W=TEX_W,TEX_H=TEX_H
        )
        #---------sprites render---------#
        render_sprites(
            pos.x, pos.y,
            dir.x, dir.y,
            plane.x, plane.y,
            self.sprite_manager.get_array(),
            textures,
            self.buffer,
            self.ZBuffer,
            TEX_W=TEX_W,TEX_H=TEX_H
        )
        #---------returns buffer---------#
        return self.buffer
    #--------------------------------#

        