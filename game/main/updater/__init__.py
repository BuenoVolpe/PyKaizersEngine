import pygame as pg
import time
#==============================================#
from engine.utils.order_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#==============================================#
from engine.utils.log import printlog
from engine.configs import configs
#==============================================#
class Updater:
    #==============================================#
    def __init__(self):
        #----------------------------------------------#
        self.objects:list[dict] = [] #{"object":object, "name":name, "piority":num}
    #==============================================#
    def update(self, delta_time:float):
        #----------------------------------------------#
        ...
    #==============================================#
    def add_object(self, obj:object, name:str=None, priority:int=None):
        try:
            #----------------------------------------------#
            if priority is None:
                priority:int = 999 
            #----------------------------------------------#
            if name is None:
                name:str = f"{obj.__class__.__name__}.{time.time()}"
            #----------------------------------------------#
            obj_:object = dict_to_class({"object":obj, "name":name, "priority":priority})
            self.objects.append(obj_)
            self.objects:list = sort_objects(self.objects)
            #----------------------------------------------#
            printlog.success(f"image {name} was added to updater's images")
        #----------------------------------------------#
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"image cannot add {name} to updater's images; \n {e}")
    #==============================================#
    def remove(self, name:str):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            for object in self.objects.copy():
                #----------------------------------------------#
                if object.name == name:
                    self.objects.remove(object)
            #----------------------------------------------#
            printlog.success(f"object {name} was removed fromupdater's objects")
        #----------------------------------------------#
        except Exception as e:
            printlog.error(f"object cannot remove {name} from updater's objects; \n {e}")