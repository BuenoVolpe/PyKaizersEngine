import pygame as pg
#=====================================#
from engine.configs import configs
#=====================================#
from engine.resource_string import ResourceStringManager
# from engine.signalbus import SignalBus
#=====================================#
pg.init()
#=====================================#
class GlobalClasses:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self.resource_string_manager:ResourceStringManager
        # self.signal_bus:SignalBus
#=====================================#
globalclasses:GlobalClasses = GlobalClasses()

