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
class WorldFactory:
    def __init__(self, world, entity_factory, game):
        #-------------------------------------#
        self.paths = {
            "pyk": paths.get("engine_worlds", "assets/engine/worlds/"),
            f"{settings.game_acronym}": paths.get("game_worlds", "assets/game/worlds/")
        }
        #------------------------+-------------#
        self.world_registry = {}
        self.load_registry()
        #-------------------------------------#
        self.entity_factory = entity_factory
        self.world = world
        self.game = game
    #=====================================#
    def load_registry(self):
        for origin, path in self.paths.items():
            #-------------------------------------#
            for info in scan_folder_for_json(path):
                json_path = info["json_path"]
                #-------------------------------------#
                relative = os.path.relpath(json_path, path)
                #-------------------------------------#
                world_id = (
                    relative
                    .replace(".json", "")
                    .replace("\\", ".")
                    .replace("/", ".")
                )
                #-------------------------------------#
                world_id = f"world@{origin}::{world_id}"
                #-------------------------------------#
                self.world_registry[world_id] = json_path
    #=====================================#
    def create_world(self, world_id:str):
        #-------------------------------------#
        world_path = self.world_registry.get(world_id)
        if world_path is None:
            log_error(f"world {world_id} not found")
            return
        #-------------------------------------#
        self.world.clear()
        #-------------------------------------#
        world_data = json_reader(world_path)
        #-------------------------------------#
        entities = world_data.get("entities", [])
        if entities:
            #-------------------------------------#
            for i, entity_data in enumerate(entities):
                #-------------------------------------#
                prefab = entity_data.get("prefab")
                positions = entity_data.get("positions")
                overrides = entity_data.get("overrides")
                #-------------------------------------#
                if not prefab:
                    log_error(f"entity of index {i} has no prefab")
                    continue
                if not self.entity_factory.get_path(prefab):
                    log_error(f"entity {prefab} does not exist")
                    continue
                #-------------------------------------#
                if not positions:
                    self.entity_factory.spawn_entity(prefab, overrides)
                    continue
                #-------------------------------------#
                overrides_copy = copy.deepcopy(entity_data.get("overrides", {}))
                for (x,y) in positions:
                    #-------------------------------------#
                    overrides_copy["component@pyk::Position"] = {"x":x, "y":y}
                    self.entity_factory.spawn_entity(prefab, overrides_copy)
                #-------------------------------------#

        #-------------------------------------#
        else:
            log_error(f"world {world_id} has no entities")
    #=====================================#
        


