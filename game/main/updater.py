#=====================================#
import pygame as pg
from sys import exit
#=====================================#
from engine.utils.log import log_error
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
    def update(self, delta_time:float):
        max_delta_time_value = 1
        if delta_time > max_delta_time_value:
            return
        #--------------------------------#
        # signal_bus.process()
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
