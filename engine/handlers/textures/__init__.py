from importlib.resources import path
#=====================================#
import pygame as pg
import numpy as np
import os
#=====================================#
from engine.configs.configs import configs
#-------------------------------------#
from engine.utils.json import scan_folder_with_json
#-------------------------------------#
from engine.handlers.textures.atlas import Atlas
from engine.handlers.textures.loader import Loader
from engine.handlers.textures.image_loader import ImageLoader
from engine.handlers.textures.color_map_loader import ColorMapLoader
#-------------------------------------#
from engine.utils.scaler import scaler
from engine.utils.log import log_error
from engine.utils.dict_to_class import dict_to_class
from engine.utils.recolor import recolor, darken_color
#=====================================#
class TextureHandler:
    def __init__(self):
        #-------------------------------------#
        self.paths = dict_to_class({
            configs.engine.acronym: configs.paths.engine_textures,
            configs.game.acronym: configs.paths.game_textures,
            "error": configs.paths.error_image,
            "color_map": configs.paths.color_map,
            "color_map_json": configs.paths.color_map_json,
        })
        #-------------------------------------#
        self.image_loader = ImageLoader()
        self.color_map_loader = ColorMapLoader(self.image_loader)
        self.color_maps = self.color_map_loader.load(self.paths.color_map, self.paths.color_map_json)
        #-------------------------------------#
        self.atlas = Atlas(
            self.image_loader.load(self.paths.error)
            # pg.image.load(self.paths["error"]).convert()
        )
        #-------------------------------------#
        self.loader = Loader(self.atlas, self.image_loader, self.paths, self.color_maps)
    #================================#
    def get(self, name: str):
        """
        Main public API:
        Retrieves any sprite from the atlas.
        """
        return self.atlas.get(name)
    #================================#
    def random(self):
        return self.atlas.random()
    #================================#
    def blit(self, name: str, target:object, pos:tuple=None):
        """
        Blits a sprite onto a target surface at a given position.
        """
        sprite = self.get(name)
        #-------------------------------------#
        if not pos:
            pos = configs.game.base_window_center
        #-------------------------------------#
        target.blit(sprite, pos)
    #================================#
    def blit_random(self, target:object, pos:tuple=None):
        """
        Blits a random sprite onto a target surface at a given position.
        """
        sprite = self.random()
        #-------------------------------------#
        if not pos:
            pos = configs.game.base_window_center
        #-------------------------------------#
        target.blit(sprite, pos)

