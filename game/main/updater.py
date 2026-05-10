from engine.handlers.textures import TextureHandler
from engine.configs.settings import settings
#--------------------------------#
from engine.utils.log import log_error
from engine.utils.event_bus import event_bus
from game.fonts import *
#--------------------------------#
from engine.ecs.systems.all import *
#--------------------------------#
from game.enums.events import events
from game.enums.update_priotitys import update_priotitys
#--------------------------------#
import pygame as pg
#=====================================#
class Updater:
    #--------------------------------#
    def __init__(self, world):
        #--------------------------------#
        self.objects = {} #priority: [elements]
        self.systems = [ #[sys1, sys2(value, key), sys3(kwarg="aa")]
            PlayerInputSystem(world),
            SimpleMovementSystem(world)
        ] 
        #--------------------------------#
        event_bus.subscribe(events.ADD_OBJECT_UPDATE, self.add_object, priority=3)
        event_bus.subscribe(events.REMOVE_OBJECT_UPDATE, self.remove_object, priority=3)
    #=====================================#
    def add_object(self, obj:object, priority:int=0):
        #--------------------------------#  
        if priority not in self.objects:
            self.objects[priority] = []
        #--------------------------------#
        self.objects[priority].append(obj)
    #--------------------------------#
    def remove_object(self, obj:object):
        for priority in self.layers:
            if obj in self.layers[priority]:
                self.layers[priority].remove(obj)
                return
    #=====================================#
    def update(self, delta_time:float):
        #--------------------------------#
        for system in self.systems:
            system.update(delta_time)
        #--------------------------------#
        for priority in sorted(self.objects.keys()):
            for obj in self.objects[priority]:
                #--------------------------------#
                if hasattr(obj, "update"):
                    obj.update(delta_time)
                    continue
                #--------------------------------#
                log_error(f"Object {obj} has no 'update' method.")


