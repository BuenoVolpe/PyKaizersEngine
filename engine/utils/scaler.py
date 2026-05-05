import pygame as pg
from engine.configs.settings import settings
#------------------------------#
class Scaler:
    """
    Handles resolution scaling for the game.

    This class converts values and surfaces from base resolution
    into the current window resolution.
    """
    #------------------------------#
    def __init__(self):
        #------------------------------#
        self.update()
    #------------------------------#
    def update(self):
        #------------------------------#
        # Ratio between current window size and base window size
        self.W_RATIO = settings.window_width / settings.base_window_width
        self.H_RATIO = settings.window_height / settings.base_window_height
    #------------------------------#
    def constant(self, value: float) -> int:
        return int(value * settings.scale_constant * min(self.W_RATIO, self.H_RATIO))
    #------------------------------#
    def scale(self, value: float) -> int:
        return int(value * min(self.W_RATIO, self.H_RATIO))
    #------------------------------#
    def surface(self, image: pg.Surface, resolution="auto") -> pg.Surface:
        #------------------------------#
        if resolution is None:
            return image
        #------------------------------#
        # Auto scaling based on original surface size
        if resolution == "auto":
            #------------------------------#
            w = self.constant(image.get_width())
            h = self.constant(image.get_height())
            #------------------------------#
            return pg.transform.scale(image, (w, h))
        #------------------------------#
        # Manual scaling based on custom resolution
        w = self.constant(resolution[0])
        h = self.constant(resolution[1])
        #------------------------------#
        return pg.transform.scale(image, (w, h))
    #------------------------------#
    def coordenates(self, x,y) -> list[int, int]:
        #------------------------------#
        scalled_x = int(self.W_RATIO * x)
        scalled_y = int(self.H_RATIO * y)
        #------------------------------#
        return (scalled_x, scalled_y)
    #------------------------------#
    def descale_constant(self, value: float) -> int:
        #------------------------------#
        return int(value / (settings.scale_constant * min(self.W_RATIO, self.H_RATIO)))
    #------------------------------#
    def descale_coordinates(self, x, y) -> tuple[int, int]:
        #------------------------------#
        base_x = int(x / self.W_RATIO)
        base_y = int(y / self.H_RATIO)
        #------------------------------#
        return base_x, base_y
#------------------------------#
scaler = Scaler()
#------------------------------#
