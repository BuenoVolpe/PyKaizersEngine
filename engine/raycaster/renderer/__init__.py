import numpy as np
import pygame as pg
#--------------------------------#
from engine.configs.settings import settings
#--------------------------------#
from engine.raycaster.renderer.renderer_sprites import render_sprites
from engine.raycaster.renderer.walls_renderer import render_walls
from engine.raycaster.renderer.floor_ceiling_render import render_floor_ceiling

type array =  np.array
type array_surf =  np.array
type surface =  pg.Surface
#================================#
class RaycasterRenderer:
    #--------------------------------#
    def __init__(self, game, surface_w, surface_h):
        #--------------------------------#
        self.buffer = np.zeros((surface_h, surface_w), dtype=np.uint32)
        self.zbuffer = np.zeros(surface_w, dtype=np.float64)
        #--------------------------------#
        self.game = game
        self.TextureHandler = game.TextureHandler
        #--------------------------------#
        # self.floorDefaultTex1 = self.TextureHandler.get_raycaster_texture_id(settings.get("floorDefaultTex1", "texture@pyk::raycaster.mine::grass"))
        # self.floorDefaultTex2 = self.TextureHandler.get_raycaster_texture_id(settings.get("floorDefaultTex2", "texture@pyk::raycaster.mine::grass"))
        # self.ceilDefaultTex = self.TextureHandler.get_raycaster_texture_id(settings.get("ceilDefaultTex", "texture@pyk::raycaster.mine::pine_planks"))
    #================================#
    def render(self, camera:object, world:object, textures:array_surf, sprites:array, TEX_W = settings.get("texture_size", 32),TEX_H = settings.get("texture_size", 32)):
        #---------cleans buff---------#
        self.buffer[:] = 0
        self.zbuffer[:] = 1e30  # infinito'
        #---------floor and ceiling render---------#camera:object, world:object, textures:array_surf, sprites:array
        render_floor_ceiling(
            camera.pos[0], camera.pos[1],
            camera.dir[0], camera.dir[1],
            camera.plane[0], camera.plane[1],
            textures, 
            self.buffer,
            self.zbuffer,
            world.ceil_grid, world.floor_grid,
            floorDefaultTex1 = world.floorDefaultTex1, floorDefaultTex2 = world.floorDefaultTex2, ceilDefaultTex = world.ceilDefaultTex,
            TEX_W=TEX_W,TEX_H=TEX_H

        )
        #---------walls render---------#
        render_walls(
            camera.pos[0], camera.pos[1],
            camera.dir[0], camera.dir[1],
            camera.plane[0], camera.plane[1],
            world.grid,
            textures,
            self.buffer,
            self.zbuffer,
            world.thin_walls,
            world.doorsMap,
            TEX_W,TEX_H
        )
        #---------sprites render---------#
        render_sprites(
            camera.pos[0], camera.pos[1],
            camera.dir[0], camera.dir[1],
            camera.plane[0], camera.plane[1],
            sprites,#.get(),
            textures,
            self.buffer,
            self.zbuffer
        )
        #---------returns buffer---------#
        return self.buffer
    
