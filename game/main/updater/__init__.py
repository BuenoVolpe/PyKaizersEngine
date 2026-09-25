import pygame as pg
import time
#==============================================#
from engine.utils.sort_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#==============================================#
from engine.utils.log import printlog
# from engine.configs import configs
#==============================================#
# from engine.signal_bus import signal_bus
# from game.enums.signals import signals
# from game.enums.signals_priotity import signals_priority as sigprio
#==============================================#
class Updater:
    #==============================================#
    def __init__(self):
        #----------z------------------------------------#
        self.objects:list[dict] = [] #{"object":object, "name":name, "piority":num}
        #----------z------------------------------------#
        # signal_bus.subscribe(signals.UPDATER_ADD_OBJECT, self.add_object, priority=sigprio.ADD_OBJ)
        # signal_bus.subscribe(signals.UPDATER_REMOVE_OBJECT, self.remove_object, priority=sigprio.REMOVE_OBJ)
    #==============================================#
    def update(self, delta_time:float):
        # signal_bus.emit(signals.ENGINE_UPDATE, delta_time=delta_time)
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
    def remove_object(self, name:str):
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