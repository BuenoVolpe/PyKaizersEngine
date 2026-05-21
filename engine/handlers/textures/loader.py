import pygame as pg
from engine.utils.recolor import apply_multi_colorkey
from engine.configs.settings import settings

pg.init()

class ImageLoader:
    """
    Responsible only for loading images from disk.
    Keeps pygame loading logic isolated.
    """
    def load(self, path: str, alpha=True, use_color_key:bool=False) -> pg.Surface:
        """
        Loads an image and converts it for fast rendering.

        alpha=True  -> convert_alpha() (supports transparency)
        alpha=False -> convert()       (faster, no transparency)
        """
        if use_color_key:
            image = pg.image.load(path).convert()
            image = apply_multi_colorkey(image, [settings.set("color_key1", [255,0,255]), settings.get("color_key2", [175, 0, 175])])
            return image

        if alpha:
            return pg.image.load(path).convert_alpha()
    
        return pg.image.load(path).convert()

        