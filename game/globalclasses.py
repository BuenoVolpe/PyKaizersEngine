import pygame as pg
#=====================================#
from engine.configs import configs
#=====================================#
from engine.resource_string import ResourceStringManager
#=====================================#
pg.init()
#=====================================#
class GlobalClasses:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self.resource_string_manager:ResourceStringManager
#=====================================#
globalclasses:GlobalClasses = GlobalClasses()

