from importlib.resources import path

import pygame as pg
import os
#--------------------------------#
from engine.handlers.textures.loader import ImageLoader
from engine.handlers.textures.atlas import AtlasStorage
from engine.handlers.textures.color_map_loader import ColorMapLoader
from engine.handlers.textures.sheet_loader import SheetLoader
    #--------------------------------#
from engine.configs.paths import paths
from engine.configs.settings import settings
    #--------------------------------#
from engine.utils.json import scan_folder_with_json
# from engine.utils.json import json, json_reader, json_writer, scan_folder, scan_folder_for_json, scan_folder_with_json
#--------------------------------#
from engine.utils.log import log_error
from engine.utils.recolor import recolor, darken_color
from engine.utils.scaler import scaler
#================================#
class TextureHandler:
    def __init__(self):
        #--------------------------------#
        self.loader = ImageLoader()
        #--------------------------------#
        self.paths = {
            "pykaizers": paths.get("engine_textures", "assets/engine/textures/"),
            f"{settings.game_acronym}": paths.get("game_textures", "assets/game/textures/")
        }
        #--------------------------------#
        self.atlas = AtlasStorage(
            self.loader.load(paths.get("error_image", "error.png"))
        )
        #--------------------------------#
        self.color_maps = ColorMapLoader(self.loader).load(paths.get("color_map"), paths.get("color_map_json"))
        #--------------------------------#]
        self.sheet_loader = SheetLoader(self.loader, self.atlas)
        #--------------------------------#]
        for key, path in self.paths.items():
            self._load_all(path, key)
    #--------------------------------
    def _load_all(self, path: str, base="pykaizers"):
        """
        Scans the sprite folder and loads everything into the atlas.
        """
        for info in scan_folder_with_json(path):
            image_path = info["image_path"]
            meta = info["metadata"]

            # Load raw sprite texture
            sprite = self.loader.load(
                image_path,
                meta.get("convert_alpha", True),
                meta.get("use_colorkey", False)
            )

            # Convert file path into atlas key
            atlas_path = os.path.relpath(image_path, path)
            atlas_path = atlas_path.replace(".png", "").replace("\\", ".")
            if base != "pykaizers":
                atlas_path = f"texture@{base}::{atlas_path}"
            else:
                atlas_path = f"texture@pyk::{atlas_path}"

            # Sprite sheet handling
            if meta.get("type") == "sheet":
                self.sheet_loader.load(sprite, meta, self.color_maps, atlas_path)
                continue

            # Normal sprite handling
            #--------------------------------#
            if colors := meta.get("colors"):
                #--------------------------------#
                sprite = self.resize(sprite, meta)
                self.atlas.save(atlas_path + f".standart", sprite)
                #--------------------------------#
                for color in colors:
                    #--------------------------------#
                    if color in self.color_maps:
                        #--------------------------------#
                        sprite = recolor(sprite, self.color_maps[color])  
                        sprite = self.resize(sprite, meta)
                        #--------------------------------#
                        self.atlas.save(atlas_path + f".{color}", sprite)
                    else:
                        #--------------------------------#
                        log_error(f"Color map '{color}' specified for '{atlas_path}' not found in color maps.")
            #--------------------------------
            self.atlas.save(atlas_path, sprite)

    def resize(self, sprite, meta):
        meta_resize = meta.get("resize", "auto")
        meta_use_scale_constant = meta.get("use_scale_constant", False)
        sprite = scaler.surface(sprite, meta_resize, use_scale_constant=meta_use_scale_constant)
        return sprite

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
    def blit(self, name: str, target:object, pos:tuple):
        """
        Blits a sprite onto a target surface at a given position.
        """
        sprite = self.get(name)
        target.blit(sprite, pos)
    #================================#
    def blit_random(self, target:object, pos:tuple):
        """
        Blits a random sprite onto a target surface at a given position.
        """
        sprite = self.random()
        target.blit(sprite, pos)
