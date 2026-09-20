from engine.configs.base import ConfigsBase
#================================#
class Settings(ConfigsBase):
    def __init__(self, path:str="assets/configs/settings.json"):
        self.asset_marks = None
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential game if they are not provided in the JSON"""
        self.max_fps = getattr(self,"max_fps", 60)
        self.show_fps_in_title = getattr(self,"show_fps_in_title", True)
        self.window_size = getattr(self,"window_size", [640,360])
        self.full_screen = getattr(self,"full_screen", False)
#================================#
# engine = Engine()
#--------------------------------#
