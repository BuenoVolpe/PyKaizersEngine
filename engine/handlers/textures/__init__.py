from importlib.resources import path

import pygame as pg
import numpy as np
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
from engine.console import console
from engine.utils.event_bus import event_bus
from game.enums.events import events
from game.enums.event_priority import event_prioritys
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
        #--------------------------------#]
        event_bus.subscribe(events.CHANGE_RENDER_3D, self.change_3d_textures, priority=event_prioritys.IMPORTANT_RESPONSE)

    #--------------------------------
    def change_3d_textures(self, **kwargs):
        print("a")
        self.set_texture_as_raycaster_texture("texture@pyk::error")
        #-----------------------------------------------#
        for original_key, sprite in self.atlas.data.items():
            #-----------------------------------------------#
            #* texture, origin, sheet, idle.standart
            #*texture@pyk::dave_sheet:: *idle.standart*
            #-----------------------------------------------#
            key = original_key.replace("texture@", "")
            key = key.replace("pyk::", "")
            key = key.replace(f"{settings.get("game_acronym"), "pykinst"}::", "")
            key = key.replace("::", ".")
            #-----------------------------------------------#
            key_list = key.split(".")
            if "raycaster" in key_list:
                self.set_texture_as_raycaster_texture(original_key)
        self.atlas.raycaster_textures = np.array(self.atlas.raycaster_textures)
                
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
                        log_error(f"Color map '{color}' specified for '{atlas_path}' not found in color maps.", console)
            #--------------------------------
            self.atlas.save(atlas_path, sprite)

    def resize(self, sprite, meta):
        meta_resize = meta.get("resize", "auto")
        meta_use_scale_constant = meta.get("use_scale_constant", False)
        sprite = scaler.surface(sprite, meta_resize, use_scale_constant=meta_use_scale_constant)
        return sprite

    #--------------------------------#
    def is_texture_size(self, sprite):
        #-------------------#
        texture_size = settings.get("texture_size", 32)
        #-------------------#
        texture = self.get(sprite)
        #-------------------#
        if texture.get_height() != texture_size:
            return False
        if texture.get_width() != texture_size:
            return False
        #-------------------#
        return True
    
    def set_texture_to_correct_size(self, sprite):
        #--------------------------------#
        if self.is_texture_size:
            #--------------------------------#
            texture = self.get(sprite)
            self.atlas.save(sprite, texture)
            return texture
        #--------------------------------#
        texture = self.get(sprite)
        texture_size = settings.get("texture_size", 32)
        #--------------------------------#
        meta = {
            "resize": [texture_size, texture_size],
            "use_scale_constant": False
        }
        #--------------------------------#
        resized_sprite = self.resize(texture, meta)
        self.atlas.save(resized_sprite, texture)
        return resized_sprite

    def set_texture_to_array(self, surf):
        arr = pg.surfarray.pixels3d(surf).copy()
        arr = np.transpose(arr, (1,0,2)).astype(np.uint8)

        rgb32 = (
            (arr[:,:,0].astype(np.uint32) << 16) |
            (arr[:,:,1].astype(np.uint32) << 8) |
            arr[:,:,2].astype(np.uint32)
        )

        return rgb32

    def set_texture_as_raycaster_texture(self, key):
        raycater_texture = self.set_texture_to_correct_size(key)
        raycater_texture = self.set_texture_to_array(raycater_texture)
        #--------------------------------#
        self.atlas.raycaster_textures_count += 1
        #--------------------------------#
        self.atlas.raycaster_textures_id[key] = self.atlas.raycaster_textures_count
        self.atlas.raycaster_textures_keys.append(key) 
        #--------------------------------#         
        self.atlas.raycaster_textures.append(raycater_texture) 
        

    #================================#
    def get(self, name: str):
        """
        Main public API:
        Retrieves any sprite from the atlas.
        """
        return self.atlas.get(name)
    #================================#
    def get_raycaster_texture_path(self, id:int):
        return self.atlas.get_raycaster_texture_path(id)
    def get_raycaster_texture_id(self, name: str):
        return self.atlas.get_raycaster_texture_id(name)
    def get_raycaster_texture_by_id(self, id:int):
        return self.atlas.get_raycaster_texture_id(int)
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
