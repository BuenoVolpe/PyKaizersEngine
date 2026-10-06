import pygame as pg
import time
from sys import exit
#=====================================#
from engine.configs import configs
from engine.utils.log import printlog
#=====================================#
from engine.resource_string.resource_reference import ResourceReference
from engine.resource_string.parser import ResourceStringParser
#=====================================#
class ResourceStringManager:
    #=====================================#
    def __init__(self):
        self.seps = configs.engine.resource_strings_seps
        self._parser:ResourceStringParser = ResourceStringParser()
    #-------------------------------------#
    def parse(self, resource_string:str) -> ResourceReference:
        return self._parser.parse(resource_string)
#-------------------------------------#

    
    
    
    

