from engine.configs.base import ConfigsBase
from engine.utils.dict_to_class import dict_to_class
#================================#
class Engine(ConfigsBase):
    def __init__(self, path:str="assets/configs/engine.json"):
        # self.asset_marks = None
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential game if they are not provided in the JSON"""
        self.resource_type_marks = getattr(self,"resource_type_marks", dict_to_class({}))
        self.resource_strings_seps = getattr(self,"resource_strings_seps", dict_to_class({}))
        self.version = getattr(self,"version", "0.0.0.0")
        self.name = getattr(self,"name", "PyKaizersEngines")
        self.acronym = getattr(self,"acronym", "pyk")
#================================#
# engine = Engine()
#--------------------------------#