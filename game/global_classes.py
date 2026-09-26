#============================================================#
from engine.configs import configs
#============================================================#
from engine.resources_string import ResourceStringManager
from game.main.display import Display
#============================================================#
class GlobalClasses:
    def __init__(self):
        #------------------------------------------------------------#
        self.display:Display
        self.resources_string_manager:ResourceStringManager
        #------------------------------------------------------------#
        
#------------------------------------------------------------#
globalclasses:GlobalClasses = GlobalClasses()