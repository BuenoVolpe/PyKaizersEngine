import random
import os
import copy
#=====================================#
from engine.utils.json import json_reader, scan_folder_for_json
from engine.utils.log import *
#-------------------------------------#
from engine.configs.paths import paths
from engine.configs.settings import settings
#-------------------------------------#
from engine.ecs.components import COMPONENT_REGISTRY
from engine.ecs.components.all import *
from engine.ecs.systems.all import *
#=====================================#
class EntityFactory:
    def __init__(self, world, game):
        #-------------------------------------#
        self.paths = {
            "pyk": paths.get("engine_entities", "assets/engine/entities/"),
            f"{settings.game_acronym}": paths.get("game_entities", "assets/game/entities/")
        }
        #------------------------+-------------#
        self.entity_registry = {}
        self.load_registry()
        #-------------------------------------#
        self.world = world
        self.game = game
        #-------------------------------------#
        self.component_map = COMPONENT_REGISTRY
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
                if origin == "game":
                    origin = settings.game_acronym
                elif origin == "engine":
                    origin = "pyk"
                #-------------------------------------#
                entity_id = f"entity@{origin}::{entity_id}"
                #-------------------------------------#
                self.entity_registry[entity_id] = json_path    
    #=====================================#
    def create_entities(self):
        #-------------------------------------#
        for path in self.paths.values():
            objects = scan_folder_for_json(path)
            #-------------------------------------#
            for obj_info in objects:
                #-------------------------------------#
                object_path = obj_info.get("json_path")
                self.create_entity_from_json(object_path)
    #=====================================#
    def create_entity_from_json(self, json_path: str):
        json_data = json_reader(json_path)
        #-------------------------------------#
        return self.build_entity_from_data(json_data)
    #=====================================#
    def get_path(self, name: str):
        path = self.entity_registry.get(name)
        #-------------------------------------#
        if not path:
            log_error(f"entity {name} does not exist!")
            return
        #-------------------------------------#
        return path
    def create_entity(self, name: str):
        #-------------------------------------#
        name = name.replace(".", "/")
        prefix, name_ = name.split("::")
        origin = prefix.replace("entity@", "")
        #-------------------------------------#
        if origin == "engine":
            origin = "pyk"
        elif origin == "game":
            origin = settings.game_acronym
        #-------------------------------------#
        if not self.paths.get(origin):
            log_error(f"cannot find entity: {name} with origin {origin}")
            return
        #-------------------------------------#
        json_path = f"{self.paths[origin]}/{name_}.json"
        json_data = json_reader(json_path)
        #-------------------------------------#
        return self.build_entity_from_data(json_data)
    #=====================================#
    def resolve_extends(self, data):
        #-------------------------------------#
        parent_name = data.get("extends")
        #-------------------------------------#
        if not parent_name:
            return data
        #-------------------------------------#
        parent_path = self.entity_registry.get(parent_name)
        #-------------------------------------#
        if not parent_path:
            #-------------------------------------#
            log_error(f"Parent entity {parent_name} not found")
            return data
        #-------------------------------------#
        parent_data = json_reader(parent_path)
        #-------------------------------------#
        parent_data = self.resolve_extends(parent_data)
        #-------------------------------------#
        merged = deep_merge(parent_data, data)
        #-------------------------------------#
        merged.pop("extends", None)
        #-------------------------------------#
        return merged
    #=====================================#
    def build_entity_from_data(self, data, do_log_errors=True):
        entity = self.world.create_entity()
        #-------------------------------------#
        data = self.resolve_extends(data)
        #-------------------------------------#
        components = copy.deepcopy(data.get("components", {}))
        extends = copy.deepcopy(data.get("extends"))
        #-------------------------------------#
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
                log_error(f"can't find Component: {comp_name}")
        #-------------------------------------#
        if do_log_errors and errors:
            log_error(f"find {errors} errors, while creating entity")
        return entity
    #=====================================#
    def spawn_entity(self, name: str, overrides: dict | None = None):
        #-------------------------------------#
        name = name.replace(".", "/")
        prefix, name_ = name.split("::")
        #-------------------------------------#
        origin = prefix.replace("entity@", "")
        if origin == "engine":
            origin = "pyk"
        elif origin == "game":
            origin = settings.game_acronym
        #-------------------------------------#
        if not self.paths.get(origin):
            log_error(f"cannot find entity: {name} with origin {origin}")
            return
        #-------------------------------------#
        json_path = f"{self.paths[origin]}/{name_}.json"
        json_data = json_reader(json_path)
        #-------------------------------------#
        entity = self.build_entity_from_data(json_data)
        #-------------------------------------#
        if overrides:
            self.apply_overrides(entity, overrides)
        #-------------------------------------#
        return entity
    #=====================================#
    def apply_overrides(self, entity, overrides: dict):
        """
        overrides format:
        {
            "Transform": {"x": 10, "y": 20},
            "Health": {"value": 999}
        }
        """
        #-------------------------------------#
        for comp_name, values in overrides.items():
            #-------------------------------------#
            comp_class = self.component_map.get(comp_name)
            #-------------------------------------#
            if not comp_class:
                log_error(f"Override component not found: {comp_name}")
                continue
            #-------------------------------------#
            storage = self.world.get_storage(comp_class)
            component = storage.get(entity) if storage else None
            #-------------------------------------#
            if component:
                #-------------------------------------#
                for k, v in values.items():
                    setattr(component, k, v)
            #-------------------------------------#
            else:
                #-------------------------------------#
                component = comp_class(**values)
                self.world.add_component(entity, component)
#=====================================#
def validate_component(comp_class, data):
    #-------------------------------------#
    try:
        #-------------------------------------#
        comp_class(**data)
    #-------------------------------------#
    except Exception as e:
        #-------------------------------------#
        log_error(f"Error at Component {comp_class.__name__}: {e}")
        return False
    #-------------------------------------#
    return True
#=====================================#
def deep_merge(base: dict, override: dict):
    #-------------------------------------#
    result = copy.deepcopy(base)
    #-------------------------------------#
    for key, value in override.items():
        #-------------------------------------#
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
        #-------------------------------------#
            result[key] = deep_merge(result[key], value)
        #-------------------------------------#
        else:
            result[key] = copy.deepcopy(value)
        #-------------------------------------#
    return result
        


