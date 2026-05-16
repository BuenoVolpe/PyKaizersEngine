from engine.configs.paths import paths
#------------------------------#
import pygame as pg

from engine.utils.log import log_error
from engine.utils.scaler import scaler
#================================#
pg.init()
#================================#
class Font:
    def __init__(self, path:str):
        self.path = path
        #------------------------------#
        self.fonts = {}
        #------------------------------#
        for i in range(1, 101):  # Example: Create fonts for sizes 1 to 100
            self.fonts[i] = pg.font.Font(path, scaler.constant(i))
            setattr(self, f"size_{i}", self.fonts[i])  # Set attributes like size_10, size_20, etc.
        #------------------------------#
        self.size_10 = pg.font.Font(path, scaler.constant(10))
        self.size_20 = pg.font.Font(path, scaler.constant(20))
        self.size_30 = pg.font.Font(path, scaler.constant(30))

    def get_size(self, size):
        font = getattr(self, f"size_{size}")
        if not font:
            log_error(f"cannot find size {size}, returning size 10")
            return self.size_10
        return font

    def render(self, surface:pg.Surface, pos:tuple[int, int], text:str, size:int=10, color:tuple[int, int, int]=(255,255,255)):
        font = self.fonts.get(size, self.size_10)  # Get the font of the requested size, or default to size_10
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

#================================#
AtariSmall = Font(paths.get("AtariSmall"))
dogicapixel = Font(paths.get("dogicapixel"))
PixelOperator = Font(paths.get("PixelOperator"))
#================================#
fonts = {"atarismall":AtariSmall,
         "dogicapixel":dogicapixel,
         "pixeloperator":PixelOperator
}

