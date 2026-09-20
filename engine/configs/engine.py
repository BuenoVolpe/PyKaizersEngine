from engine.configs.base import ConfigsBase
#================================#
class Engine(ConfigsBase):
    def __init__(self, path:str="assets/configs/engine.json"):
        self.asset_marks = None
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential game if they are not provided in the JSON"""
        self.version = getattr(self,"version", "0.0.0.0")
        self.name = getattr(self,"name", "PyKaizersEngines")
        self.acronym = getattr(self,"acronym", "pyk")
#================================#
# engine = Engine()
#--------------------------------#
