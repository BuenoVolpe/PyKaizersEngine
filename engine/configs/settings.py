from engine.configs import Configs
from engine.configs.paths import paths
#================================#
class Settings(Configs):
    def __init__(self, path:str=paths.settings):
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential settings if they are not provided in the JSON"""
        self.window_title = getattr(self, "window_title", "PyKaizersEngine")
        #--------------------------------#
        self.engine_version = getattr(self, "engine_version", "error: missing engine_version")
        self.game_version = getattr(self, "game_version", "error: missing game_version")
        #--------------------------------#
        self.window_width, self.window_height = self.window_size = getattr(self, "window_size", [640, 360])
        self.base_window_width, self.base_window_height = self.base_window_size = getattr(self, "base_window_size", [640, 360])
        self.base_window_width_center, self.base_window_height_center = self.base_window_center = (self.base_window_width//2, self.base_window_height//2)
        self.window_width_center, self.window_height_center = self.window_center = (self.window_width//2, self.window_height//2)
        #--------------------------------#
        self.fullscreen = getattr(self, "fullscreen", False)
#--------------------------------#
settings = Settings(paths.settings)
#--------------------------------#
# settings.get(key="window_title", default="PyKaizersEngine")
# settings.set(key="window_title", value="PyKaizersEngine")


