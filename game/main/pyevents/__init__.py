import pygame as pg
from sys import exit
from typing import Any
#============================================================#
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
from engine.utils.sort_list import sort_objects
#============================================================#
from game.main.pyevents.handle_pyevents import (
    handle_KEYDOWN, handle_KEYUP, handle_MOUSEBUTTONDOWN,
    handle_MOUSEBUTTONUP, handle_MOUSEMOTION, handle_MOUSEWHEEL
)
#============================================================#
class PyEvents:
    #------------------------------------------------------------#
    def __init__(self):
        #------------------------------------------------------------#
        self.objects:list[dict] = [] #{"object":object, "name":name, "piority":num}
        #------------------------------------------------------------#
    #============================================================#
    def quit(self, event:pg.event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_LALT):
            #------------------------------------------------------------#
            pg.quit()
            exit()
    #============================================================#
    def handle(self) -> dict:
        #------------------------------------------------------------#
        events:list = pg.event.get()
        results:dict = []
        #------------------------------------------------------------#
        for event in events:
            #------------------------------------------------------------#
            result = None
            #------------------------------------------------------------#
            self.quit(event)
            #------------------------------------------------------------#
            if event.type == pg.KEYDOWN:
                result:Any = handle_KEYDOWN(event)
            elif event.type == pg.KEYUP:
                result:Any = handle_KEYUP(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                result:Any = handle_MOUSEBUTTONDOWN(event)
            elif event.type == pg.MOUSEBUTTONUP:
                result:Any = handle_MOUSEBUTTONUP(event)
            elif event.type == pg.MOUSEMOTION:
                result:Any = handle_MOUSEMOTION(event)
            elif event.type == pg.MOUSEWHEEL:
                result:Any = handle_MOUSEWHEEL(event)
            #------------------------------------------------------------#
            if result is not None:
                results.append(result)
        #==============================================#
        return {
            "events":pg.event.get(),
            "results": results
        }
        #----------------------------------------------#
    #============================================================#
    def add_object(self, obj:object, name:str=None, priority:int=None):
        #----------------------------------------------#
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
            printlog.success(f"object {name} was added from event_handler's objects")
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"object cannot add {name} from event_handler's objects; \n {e}")
    #==============================================#
    def remove_object(self, name:str):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            for object in self.objects.copy():
                #----------------------------------------------#
                if object.name == name:
                    self.objects.remove(object)
                printlog.success(f"object {name} was removed from event_handler's objects")
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"object cannot remove {name} from event_handler's objects; \n {e}")

#============================================================#