import random
import os
import copy
#=====================================#
from engine.utils.json import json_reader, scan_folder_for_json
from engine.utils.debug_log import debug_log
from engine.utils.overlay import debug_overlay
from engine.utils.log import log_error
from engine.utils.dict_to_class import dict_to_class
#-------------------------------------#
from engine.configs.configs import configs
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#-------------------------------------#
from engine.ecs.component_storage import COMPONENT_REGISTRY
from engine.ecs.components.all import *
from engine.ecs.systems.all import *
#=====================================#
class EntityFactory:
    def __init__(self, world):
        #-------------------------------------#
        self.paths = {
            configs.engine.acronym: configs.paths.engine.enities,
            configs.game.acronym: configs.paths.game.enities,
        }
        #-------------------------------------#
        self.entity_registry = {}
        self.load_registry()
        #-------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.entities_keys", 
                value=list(self.entity_registry.keys())
                )
        #-------------------------------------#
        self.world = world
        #-------------------------------------#
        self.component_map = COMPONENT_REGISTRY
        #-------------------------------------#
        # self.entity_templates = {}
        # self.load_entity_templates()
    #=====================================#
    def load_registry(self):
        for origin, path in self.paths.items():
            #-------------------------------------#
            for info in scan_folder_for_json(path):
                json_path = info["json_path"]
                #-------------------------------------#
                relative = os.path.relpath(json_path, path)
                #-------------------------------------#
                entity_id = (
                    relative
                    .replace(".json", "")
                    .replace("\\", ".")
                    .replace("/", ".")
                )
                #-------------------------------------#
                if origin == configs.engine.acronym:
                    entity_id = f"{assetsmarks.engine.entity}::{entity_id}"
                else:
                    entity_id = f"{assetsmarks.engine.game}::{entity_id}"
                #-------------------------------------#
                self.entity_registry[entity_id] = json_path    
    #=====================================#
    def create_entity(self, entity_name:str):
        json_path = self.entity_registry.get(entity_name)
        #-------------------------------------#
        json_data = json_reader(json_path)
        #-------------------------------------#
        return self.build_entity_from_data(json_data)
    #=====================================#
    def build_entity_from_data(self, data, do_log_errors:bool=True):
        #-------------------------------------#
        entity = self.world.create_entity()
        #-------------------------------------#
        components = copy.deepcopy(data.get("components", {}))
        errors = 0
        #-------------------------------------#
        for comp_name, comp_values in components.items():
            #-------------------------------------#
            comp_class = self.component_map.get(comp_name)
            #-------------------------------------#
            if comp_class:
                #-------------------------------------#
                if isinstance(comp_values, dict):
                    #-------------------------------------#
                    for key, value in comp_values.items():
                        #-------------------------------------#
                        if isinstance(value, dict):
                            #-------------------------------------#
                            if "choice" in value:
                                #-------------------------------------#
                                comp_values[key] = random.choice(value["choice"])
                            #-------------------------------------#
                            elif "random" in value:
                                #-------------------------------------#
                                comp_values[key] = random.randint(*value["random"])
                            #-------------------------------------#
                            elif "random_float" in value:
                                #-------------------------------------#
                                comp_values[key] = random.uniform(*value["random_float"])
                #-------------------------------------#
                if validate_component(comp_class, comp_values):
                    #-------------------------------------#
                    component = comp_class(**comp_values)
                    self.world.add_component(entity, component)
                #-------------------------------------#    
                continue
                #-------------------------------------#    
            else:
                errors += 1
                log_error(f"[ent_factory]: can't find Component: {comp_name}")
        #-------------------------------------#
        if do_log_errors and errors:
            log_error(f"[ent_factory]: find {errors} errors, while creating entity")
        return entity

#=====================================#
def validate_component(comp_class, data):
    #-------------------------------------#
    try:
        #-------------------------------------#
        comp_class(**data)
    #-------------------------------------#
    except Exception as e:
        #-------------------------------------#
        log_error(f"[ent_factory]: Error at Component {comp_class.__name__}: {e}")
        return False
    #-------------------------------------#
    return True
