from engine.configs import Configs
#================================#
class Paths(Configs):
    def __init__(self, path:str="assets/configs/paths.json"):
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential paths if they are not provided in the JSON"""
        self.configs = getattr(self, "configs", "assets/configs/")
        #--------------------------------#
        self.settings = getattr(self, "settings", "assets/configs/settings.json")
        self.paths = getattr(self, "paths", "assets/configs/paths.json")
        #--------------------------------#
        self.fonts = getattr(self, "fonts", "assets/engine/fonts/")
        #--------------------------------#
        self.AtariSmall = getattr(self, "AtariSmall", "assets/engine/fonts/AtariSmall.ttf")
        self.dogicapixel = getattr(self, "dogicapixel", "assets/engine/fonts/dogicapixel.ttf")
        self.PixelOperator = getattr(self, "PixelOperator", "assets/engine/fonts/PixelOperator.ttf")
#================================#
paths = Paths()
#--------------------------------#

