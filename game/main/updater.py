from engine.handlers.textures import TextureHandler
from engine.configs.settings import settings
#--------------------------------#
from engine.utils.log import log_error
from engine.utils.event_bus import event_bus
from game.fonts import *
#--------------------------------#
from engine.ecs.systems.all import *
from engine.console import console
#--------------------------------#
from game.enums.events import events
from game.enums.update_prioritys import update_prioritys as priority
from game.enums.event_priority import event_prioritys as ev_priority
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
            RaycastPlayerMouseSystem(world),
            RaycasterPlayerColisionSystem(world, map=world.game.render.map),
            SimpleMovementSystem(world),
            RaycastCameraUpdateSystem(world, game=world.game),
        ] 
        #--------------------------------#
        self.pause = settings.get("start_game_paused", False)
        #--------------------------------#
        event_bus.subscribe(events.ADD_OBJECT_UPDATE, self.add_object, priority=ev_priority.ADD)
        event_bus.subscribe(events.REMOVE_OBJECT_UPDATE, self.remove_object, priority=ev_priority.REMOVE)
        event_bus.subscribe(events.PAUSE, self.pause_game, priority=ev_priority.PRE_LOGIC)
    #=====================================#
    def pause_game(self):
        self.pause = not self.pause
        #--------------------------------#  
        if self.pause:
            if not pg.mouse.get_visible():
                pg.mouse.set_visible(True)
            if pg.event.get_grab():
                pg.event.set_grab(False)
        #--------------------------------#  
        else:
            if settings.get("render3D"):
                if pg.mouse.get_visible():
                    pg.mouse.set_visible(False)
                if not pg.event.get_grab():
                    pg.event.set_grab(True)
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
        if self.pause or console.visible:
            return
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


