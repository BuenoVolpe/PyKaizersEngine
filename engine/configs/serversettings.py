from engine.configs import Configs
from engine.configs.paths import paths
#================================#
class Settings(Configs):
    def __init__(self, path:str=paths.serversettings):
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential settings if they are not provided in the JSON"""
        self.ticks = self.get("ticks", 60)
#--------------------------------#
serversettings = Settings(paths.serversettings)
#--------------------------------#
# serversettings.get(key="window_title", default="PyKaizersEngine")
# serversettings.set(key="window_title", value="PyKaizersEngine")
