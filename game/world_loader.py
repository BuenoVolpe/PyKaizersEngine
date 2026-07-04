import random
import os
import copy
#=====================================#
from engine.utils.json import json_reader, scan_folder_for_json
from engine.utils.debug_log import debug_log
from engine.utils.overlay import debug_overlay
from engine.utils.globalclasses import globalclasses
from engine.utils.log import log_error
from engine.utils.map_creator import map_create, mapping
from engine.utils.dict_to_class import dict_to_class
#-------------------------------------#
from engine.configs.configs import configs
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#=====================================#
class WorldLoader:
    def __init__(self):
        ...
        #-------------------------------------#
        signal_bus.subscribe(signals.LOAD_COMPLETE_WORLD, self.load_world, priority=signals_prioritys.LOAD)
        #-------------------------------------#
    
    def load_world(self, name:str, data:dict):
        #-------------------------------------#
        ...


