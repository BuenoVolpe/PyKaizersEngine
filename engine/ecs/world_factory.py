import random
import os
import copy
#=====================================#
from engine.utils.json import json_reader, scan_folder_for_json
from engine.utils.log import *
#-------------------------------------#
from engine.console import console
#-------------------------------------#
from engine.configs.paths import paths
from engine.configs.settings import settings
#-------------------------------------#
from engine.utils.event_bus import event_bus
from game.enums.events import events
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
        #-------------------------------------#
        event_bus.subscribe(events.CREATE_WORLD, self.create_world, priority=255)
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
        name_ = world_id.split("::")
        if len(name_) > 1:
            prefix, name_ = name_
        else:
            log_error(f"cannot find world: {world_id}", console)
            return
        #-------------------------------------#
        origin = prefix.replace("world@", "")
        if origin == "engine":
            world_id = world_id.replace("@engine::", "@pyk::")
            origin = "pyk"
        elif origin == "game":
            world_id = world_id.replace("@game::", f"@{settings.game_acronym}::")
            origin = settings.game_acronym
        #-------------------------------------#
        world_path = self.world_registry.get(world_id)
        if world_path is None:
            log_error(f"world {world_id} not found", console)
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
                    log_error(f"entity of index {i} has no prefab", console)
                    continue
                if not self.entity_factory.get_path(prefab):
                    log_error(f"entity {prefab} does not exist", console)
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
            log_error(f"world {world_id} has no entities", console)
        #-------------------------------------#
        type = world_data.get("type", "NOT_SPECIFIED")
        if type == "raycast3D":
            event_bus.emit(events.CREATE_WORLD_RAYCAST, world_data=world_data)
    #=====================================#
        


