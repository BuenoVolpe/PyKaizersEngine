#================================#
import pygame as pg
from random import choice
#================================#
from game.enums.assetsmarks import assetsmarks
from engine.configs import configs
from engine.utils.log import log_error
#================================#
class Atlas:
    def __init__(self, error_image:pg.Surface):
        self.error_image = error_image
        #--------------------------------#
        self.data = {}
        #--------------------------------#
        self.error_already_happen = False
        self.error_image = error_image
        self.save(f"{assetsmarks.engine.texture}::error", error_image)

    #================================#
    def save(self, name:str, image:pg.surface):
        #--------------------------------#
        self.data[name] = image
    #================================#
    def get(self, name:str):
        #--------------------------------#
        image = self.data.get(name)
        #--------------------------------#
        if not image:
            log_error(f"Sprite '{name}' not found in atlas. Returning error sprite.")#, True)
            return self.error_image
        #--------------------------------#
        return image
    #================================#
    def random(self):
        """
        Returns a random sprite from the atlas (debug purpose).
        """
        return choice(list(self.data.values()))


