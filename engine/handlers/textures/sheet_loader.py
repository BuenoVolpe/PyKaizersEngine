from engine.handlers.textures.atlas import AtlasStorage
from engine.handlers.textures.loader import ImageLoader
import pygame as pg

from engine.utils.scaler import scaler
from engine.utils.recolor import recolor
from engine.utils.log import log_error

class SheetLoader:
    """
    Responsible for loading sprite sheets and applying color maps to them.
    """
    def __init__(self, loader: ImageLoader, atlas: AtlasStorage):
        self.loader = loader
        self.atlas = atlas
    
    def load(self, sheet: pg.Surface, meta: dict, color_maps: dict, atlas_path: str):
        """
        Loads a sprite sheet, applies color maps, and saves the individual sprites to the atlas.
        """
        meta = meta.copy()  # Avoid mutating the original metadata
        #--------------------------------#
        if sprites := meta.get("sprites"):
            #--------------------------------#
            for sprite_name, sprite_meta in sprites.items():
                #--------------------------------#
                start = sprite_meta.get("start", [0,0])
                size = sprite_meta.get("size", [1,1])
                resize = sprite_meta.get("resize", [1,1])
                colors = sprite_meta.get("colors", [])
                use_scale_constant = sprite_meta.get("use_scale_constant", True)
                #--------------------------------#
                sprite = sheet.subsurface(pg.Rect(start, size))
                #--------------------------------#
                sprite_atlas_path = f"{atlas_path}::{sprite_name}"
                #--------------------------------#
                if colors:
                    #--------------------------------#
                    sprite = self.resize(sprite, sprite_meta)
                    self.atlas.save(sprite_atlas_path + f".standart", sprite)
                    #--------------------------------#
                    for color in colors:
                        #--------------------------------#
                        if color in color_maps:
                            #--------------------------------#
                            sprite = recolor(sprite, color_maps[color])  
                            sprite = self.resize(sprite, sprite_meta)
                            #--------------------------------#
                            self.atlas.save(sprite_atlas_path + f".{color}", sprite)
                        else:
                            #--------------------------------#
                            log_error(f"Color map '{color}' specified for '{atlas_path}' not found in color maps.")
            return
        #--------------------------------#
        log_error(f"Sprite sheet '{atlas_path}' is missing 'sprites' metadata.")
        return sheet

    def resize(self, sprite, meta):
        meta_resize = meta.get("resize", "auto")
        meta_use_scale_constant = meta.get("use_scale_constant", False)
        sprite = scaler.surface(sprite, meta_resize, use_scale_constant=meta_use_scale_constant)
        return sprite

