from engine.console import command, console
from engine.configs.settings import settings
#--------------------------------#
from engine.utils.event_bus import event_bus
from game.enums.events import events
#================================#
@command("entity.spawn", protection_level=1)
def entity_spawn(name:str, overrides=None):
    #--------------------------------#
    """spawns an entity with given name"""
    """
    overrides = {
        "component@pyk::Position": {"x":0, "y":0},
        "component@pyk::Velocity": {"x":0, "y":10, "max_velocity": [0, 10]}
    }
    """
    #--------------------------------#
    event_bus.emit(events.SPAWN_ENTITY, name=name, overrides=overrides)
    #--------------------------------#
    return f"spawned entity {name}"
#================================#
@command("entity.kill", protection_level=1)
def entity_kill(entity:int):
    """kills a entity"""
    #--------------------------------#
    event_bus.emit(events.KILL_ENTITY, entity=entity)
    #--------------------------------#
    return f"killed entity:{entity}"
#================================#
@command("load_world", protection_level=1)
def load_world(world_id):
    #--------------------------------#
    event_bus.emit(events.CREATE_WORLD, world_id=world_id)
    #--------------------------------#
    return f"created world {world_id}"


          
