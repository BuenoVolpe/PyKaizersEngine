import numpy as np
import math
import pygame as pg
#--------------------------------#
from engine.configs.configs import configs
from engine.utils.dict_to_class import dict_to_class
#--------------------------------#
from engine.raycaster3D.constants import posX, posY, dirX, dirY, planeX, planeY, TEX_H, TEX_W, worldMap, default_sprites_data, default_thin_walls, default_doors
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
        self.thin_walls = default_thin_walls
        self.sprites = default_sprites_data
        self.doorsMap = default_doors
        self.grid = worldMap
        self.ceil_grid = worldMap
        self.floor_grid = worldMap
        self.floorDefaultTex1 = 56
        self.floorDefaultTex2 = 57
        self.ceilDefaultTex = 58
        #--------------------------------#
        self.camera = dict_to_class({
            "pos": [posX, posY],
            "dir": [dirX, dirY],
            "plane": [planeX, planeY],
        })
        self.set_fov(90)
    #--------------------------------#
    def render(self, textures:array_surf):
        #---------cleans buff---------#
        self.buffer[:] = 0
        self.ZBuffer[:] = 1e30  # infinito'
        #---------floor and ceiling render---------#camera:object, world:object, textures:array_surf, sprites:array
        render_floor_ceiling(
            self.camera.pos[0], self.camera.pos[1],
            self.camera.dir[0], self.camera.dir[1],
            self.camera.plane[0], self.camera.plane[1],
            textures, 
            self.buffer,
            self.ZBuffer,
            self.ceil_grid, self.floor_grid,
            floorDefaultTex1 = self.floorDefaultTex1, floorDefaultTex2 = self.floorDefaultTex2, ceilDefaultTex = self.ceilDefaultTex,
            TEX_W=TEX_W,TEX_H=TEX_H

        )
        #---------walls render---------#
        render_walls(
            self.camera.pos[0], self.camera.pos[1],
            self.camera.dir[0], self.camera.dir[1],
            self.camera.plane[0], self.camera.plane[1],
            self.grid,
            textures,
            self.buffer,
            self.ZBuffer,
            self.thin_walls,
            self.doorsMap,
            TEX_W=TEX_W,TEX_H=TEX_H
        )
        #---------sprites render---------#
        render_sprites(
            self.camera.pos[0], self.camera.pos[1],
            self.camera.dir[0], self.camera.dir[1],
            self.camera.plane[0], self.camera.plane[1],
            self.sprites,#.get(),
            textures,
            self.buffer,
            self.ZBuffer,
            TEX_W=TEX_W,TEX_H=TEX_H
        )
        #---------returns buffer---------#
        return self.buffer
    #--------------------------------#
    def set_view_angle(self, angle_deg: float):
        angle = math.radians(angle_deg)
        #--------------------------------#
        self.camera.dir[0] = math.cos(angle)
        self.camera.dir[1] = math.sin(angle)
    #--------------------------------#
    def set_fov(self, fov_deg: float):
        angle = math.atan(math.tan(math.radians(fov_deg) / 2))

        plane_length = math.tan(math.radians(fov_deg) / 2)

        dx, dy = self.camera.dir

        # perpendicular ao vetor direção
        self.camera.plane[0] = -dy * plane_length
        self.camera.plane[1] = dx * plane_length

        