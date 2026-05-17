#--------------------------------#
from engine.ecs.components.all import *
from engine.ecs.components import ComponentStorage
#--------------------------------#
from engine.ecs.systems.all import *
#--------------------------------#
from engine.utils.event_bus import event_bus
from game.enums.events import events
#--------------------------------#
from engine.utils.event_bus import event_bus
from engine.utils.log import log, log_error, log_list, log_success
from game.enums.events import events
#================================#
class World:
    #--------------------------------------#
    def __init__(self, game):
        self.game = game
        #--------------------------------------#
        self.next_entity = 0
        #--------------------------------------#
        self.components = {}
        self.query_cache = {}
        self.sprite_to_entity = {}
        #--------------------------------------#
        self.to_remove = set()
        #--------------------------------------#
        event_bus.subscribe(events.KILL_ENTITY, self.remove_entity, priority=2)
    #================================#
    def get_component(self, entity:int, comp_type:object):
        #--------------------------------------#
        storage = self.get_storage(comp_type)
        return storage.get(entity)
    #================================#
    def create_entity(self):
        #--------------------------------------#
        eid = self.next_entity
        self.next_entity += 1
        #--------------------------------------#
        return eid
    #================================#
    def clear(self):
        #--------------------------------------#
        for storage in self.components.values():
            storage.data.clear()
        #--------------------------------------#
        self.components.clear()
        self.query_cache.clear()
        self.sprite_to_entity.clear()
        self.to_remove.clear()
        #--------------------------------------#
        self.next_entity = 0 
    #================================#
    def remove_entity(self, entity:int):
        #--------------------------------------#
        self.to_remove.add(entity)
        #--------------------------------------#
        self.query_cache.clear()
    #================================#
    def flush(self):
        #--------------------------------------#
        for entity in self.to_remove:
            #--------------------------------------#
            for storage in self.components.values():
            #--------------------------------------#
                storage.data.pop(entity, None)
        #--------------------------------------#
        self.to_remove.clear()
    #================================#
    def remove_component(self, entity:int, comp_type:object):
        #--------------------------------------#
        storage = self.get_storage(comp_type)
        storage.remove(entity)
        #--------------------------------------#
        self.query_cache.clear()
    #================================#
    def get_entity_components(self, entity:int):
        #--------------------------------------#
        comps = {}
        #--------------------------------------#
        for comp_type, storage in self.components.items():
            #--------------------------------------#
            comp = storage.get(entity)
            if comp is not None:
                comps[comp_type.__name__] = comp
            #--------------------------------------#
        return comps
    #================================#
    def get_storage(self, comp_type:object):
        #--------------------------------------#
        if comp_type not in self.components:
            #--------------------------------------#
            self.components[comp_type] = ComponentStorage()
        #--------------------------------------#
        return self.components[comp_type]
    #================================#
    def add_component(self, entity:int, component:object):
        #--------------------------------------#
        storage = self.get_storage(type(component))
        storage.add(entity, component)
        #--------------------------------------#
        self.query_cache.clear()
    #================================#
    def query(self, *include:object, exclude:tuple[object]=()):
        #--------------------------------------#
        key = (include, exclude)
        #--------------------------------------#
        if key in self.query_cache:
            #--------------------------------------#
            base, include_storages, exclude_storages = self.query_cache[key]
        #--------------------------------------#
        else:
            #--------------------------------------#
            include_storages = [self.get_storage(c) for c in include]
            exclude_storages = [self.get_storage(c) for c in exclude]
            #--------------------------------------#
            if not include_storages:
                return
            #--------------------------------------#
            base = min(include_storages, key=lambda s: len(s.data))
            #--------------------------------------#
            self.query_cache[key] = (base, include_storages, exclude_storages)
        #--------------------------------------#
        for entity in base.data:
            #--------------------------------------#
            components = []
            #--------------------------------------#
            for storage in include_storages:
                #--------------------------------------#
                comp = storage.get(entity)
                #--------------------------------------#
                if comp is None:
                    break
                #--------------------------------------#
                components.append(comp)
            #--------------------------------------#
            else:
                #--------------------------------------#
                for storage in exclude_storages:
                    #--------------------------------------#
                    if storage.has(entity):
                        #--------------------------------------#
                        break
                #--------------------------------------#
                else:
                    yield entity, tuple(components)


# world = World()
# player = world.create_entity()
# world.add_component(player, Position(0, 0))
# world.add_component(player, Velocity(10, 5))

# movement = MovementSystem()

# for _ in range(5):
#     movement.update(world, 0.016)
#     pos = world.get_storage(Position).get(player)
#     print(pos.x, pos.y)



