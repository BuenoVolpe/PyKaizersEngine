#=====================================#
import pygame as pg
#=====================================#
from engine.utils.log import log_error
#--------------------------------#
from engine.signal_bus import signal_bus
#--------------------------------#
from engine.configs.configs import configs
#=====================================#
class Updater:
    #=====================================#
    def __init__(self):
        #--------------------------------#
        self.objects = {} #priority: [elements]
        #--------------------------------#
        self.systems = [ #[sys1, sys2(value, key), sys3(kwarg="aa")]
        ] 
        #=====================================#
        self._subscribe_functions()
    #=====================================#
    def _subscribe_functions(self):
        #-------------------------------------#
        signal_bus.subscribe("signal@pyk::updater.add.object", self.add_object, priority=10)
        signal_bus.subscribe("signal@pyk::updater.remove.object", self.remove_object, priority=10)
    #=====================================#
    def update(self, delta_time:float):
        #--------------------------------#
        if delta_time > configs.engine.max_delta_time_value:
            return
        #--------------------------------#
        signal_bus.emit("signal@pyk::engine.update", dt=delta_time)
        #--------------------------------#
        signal_bus.process()
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
    #=====================================#
    def add_object(self, obj:object, priority:int=0):
        #--------------------------------#  
        if priority not in self.objects:
            self.objects[priority] = []
        #--------------------------------#
        self.objects[priority].append(obj)
    #--------------------------------#
    def remove_object(self, obj:object):
        for priority in self.objects:
            if obj in self.objects[priority]:
                self.objects[priority].remove(obj)
                return
