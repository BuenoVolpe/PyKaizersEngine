import os
import pygame as pg
#=====================================#
from engine.utils.recolor import recolor
from engine.utils.json import scan_folder_with_json
from engine.utils.scaler import scaler
from engine.utils.log import log_list, log_error
#=====================================#
from engine.configs.configs import configs
#=====================================#
pg.init()
#=====================================#
class Loader:
    def __init__(self, atlas:object, image_loader:object, paths:object, color_map:dict):
        #-------------------------------------#
        self.engine_path = getattr(paths, configs.engine.acronym)
        self.game_path = getattr(paths, configs.game.acronym)
        #-------------------------------------#
        self.paths = {
            configs.engine.acronym: self.engine_path,
            configs.game.acronym: self.game_path
        }
        #-------------------------------------#
        self.atlas = atlas
        self.image_loader = image_loader
        #-------------------------------------#
        self.color_map = color_map
        #-------------------------------------#
        self._load()
        #-------------------------------------#
        # log_list(list(self.atlas.data.keys()))
    #=====================================#
    def _load(self):
        #-------------------------------------#
        engine_asset = f"{configs.engine.asset_marks.texture}@{configs.engine.acronym}"
        game_asset = f"{configs.engine.asset_marks.texture}@{configs.game.acronym}"
        #=====================================#
        for base, path in self.paths.items():
            for info in scan_folder_with_json(path):
                #--------------------------------#
                name = info["name"]
                image_path = info["file_path"]
                json_path = info["json_path"]
                meta = info["metadata"]
                #--------------------------------#
                convert_alpha = meta.get("convert_alpha", True)
                use_colorkey = meta.get("use_colorkey", False)
                type = meta.get("type")
                colors = meta.get("colors")
                scale = meta.get("scale")
                use_constant = meta.get("use_constant", False)
                #=====================================#
                sprite = self.image_loader.load(
                    image_path,
                    convert_alpha,
                    use_colorkey
                )
                #=====================================#
                atlas_path = os.path.relpath(image_path, path)
                atlas_path = atlas_path.replace(".png", "").replace("\\", ".")
                #-------------------------------------#
                if base == configs.engine.acronym:
                    atlas_path = f"{engine_asset}::{atlas_path}"
                elif base == configs.game.acronym:
                    atlas_path = f"{game_asset}::{atlas_path}"
                #=====================================#

                if type == "sheet":
                    self._load_sheet(sprite, meta, self.color_map, atlas_path)
                    continue
                if colors:
                    self.recolor_sprite(sprite, colors, atlas_path, self.color_map, meta)
                    continue
                if scale:
                    sprite = scaler.surface(sprite, scale, use_constant)
                #-------------------------------------#
                self.atlas.save(atlas_path, sprite)

    #=====================================#
    def _load_sheet(self, sheet: pg.Surface, meta: dict, color_maps: dict, atlas_path: str):
        #-------------------------------------#
        self.atlas.save(atlas_path, sheet)
        #=====================================#
        meta = meta.copy()
        #--------------------------------#
        if sprites := meta.get("sprites"):
            for sprite_name, sprite in sprites.items():
                #--------------------------------#
                start = sprite.get("start",[0,0])
                size = sprite.get("size",[1,1])
                #--------------------------------#
                convert_alpha = sprite.get("convert_alpha", True)
                use_colorkey = sprite.get("use_colorkey", False)
                type = sprite.get("type")
                colors = sprite.get("colors")
                scale = sprite.get("scale")
                use_constant = sprite.get("use_constant", False)
                #--------------------------------#
                image = sheet.subsurface(pg.Rect(start, size))
                #--------------------------------#
                sprite_atlas_path = f"{atlas_path}::{sprite_name}"
                #--------------------------------#
                if colors:
                    self.recolor_sprite(image, colors, atlas_path, color_maps, sprite)
                    continue
                #--------------------------------#
                if scale:
                    image = scaler.surface(image, scale, use_constant)
                #--------------------------------#
                self.atlas.save(sprite_atlas_path, image)

        #-------------------------------------#
        if sprites is None:
            log_error(f"no sprites found in sheet {atlas_path}")#, True)

    def recolor_sprite(self, sprite:pg.Surface, colors:list, atlas_path:str, color_maps:dict, meta:dict={}):
        #--------------------------------#
        sprite_ = sprite
        if scale := meta.get("scale"):
            sprite_ = scaler.surface(sprite, scale, meta.get("use_constant", False))
        #--------------------------------#
        self.atlas.save(atlas_path, sprite_)
        self.atlas.save(f"{atlas_path}.standart", sprite_)
        #--------------------------------#
        for color in colors:
            #--------------------------------#
            sprite_copy = sprite.copy()
            #--------------------------------#
            if color not in color_maps:
                log_error(f"Color map '{color}' specified for '{atlas_path}' not found in color maps.")#, console)
                continue
            #--------------------------------#
            sprite_copy = recolor(sprite_copy, color_maps[color])
            #--------------------------------#
            if scale := meta.get("scale"):
                sprite_copy = scaler.surface(sprite_copy, scale, meta.get("use_constant", False))
            #--------------------------------#
            self.atlas.save(f"{atlas_path}.{color}", sprite_copy)


