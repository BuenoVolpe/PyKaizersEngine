from engine.configs.paths import paths
#------------------------------#
import pygame as pg

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
        #------------------------------#
        self.size_10 = pg.font.Font(path, scaler.constant(10))
        self.size_20 = pg.font.Font(path, scaler.constant(20))
        self.size_30 = pg.font.Font(path, scaler.constant(30))

    def render(self, surface:pg.Surface, pos:tuple[int, int], text:str, size:int=10, color:tuple[int, int, int]=(255,255,255)):
        font = self.fonts.get(size, self.size_10)  # Get the font of the requested size, or default to size_10
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

#================================#
AtariSmall = Font(paths.get("AtariSmall"))
dogicapixel = Font(paths.get("dogicapixel"))
PixelOperator = Font(paths.get("PixelOperator"))
#================================#


