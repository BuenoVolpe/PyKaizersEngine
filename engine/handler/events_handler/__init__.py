import pygame as pg
from sys import exit
from typing import Any
import time
#==============================================#
from engine.utils.order_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#==============================================#
from engine.handler.events_handler.handle_event import (
handle_event_KEYDOWN,
handle_event_KEYUP,
handle_event_MOUSEBUTTONDOWN,
handle_event_MOUSEBUTTONUP,
handle_event_MOUSEMOTION,
handle_event_MOUSEWHEEL)
#==============================================#
class EventsHandler:
    def __init__(self):
        #----------------------------------------------#
        self.objects:list[dict] = [] #{"object":object, "name":name, "piority":num}
    #==============================================#
    def events(self, engine:object) -> dict[str, list]:
        #----------------------------------------------#
        results:list = []
        #----------------------------------------------#
        for event in pg.event.get():
            result:Any = None
            #----------------------------------------------#
            if event.type == pg.QUIT:
                #----------------------------------------------#
                engine.running = False
                pg.quit()
                exit()
            #==============================================#
            elif event.type == pg.KEYDOWN:
                result:Any = handle_event_KEYDOWN(event)
            elif event.type == pg.KEYUP:
                result:Any = handle_event_KEYUP(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                result:Any = handle_event_MOUSEBUTTONDOWN(event)
            elif event.type == pg.MOUSEBUTTONUP:
                result:Any = handle_event_MOUSEBUTTONUP(event)
            elif event.type == pg.MOUSEMOTION:
                result:Any = handle_event_MOUSEMOTION(event)
            elif event.type == pg.MOUSEWHEEL:
                result:Any = handle_event_MOUSEWHEEL(event)
            # else:
                # for 
            #==============================================#
            if result is not None:
                results.append(result)
        #==============================================#
        return {
            "events":pg.event.get(),
            "results": results
        }
        #----------------------------------------------#
    #==============================================#
    def add_object(self, obj:object, name:str=None, priority:int=None):
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
    #==============================================#
    def remove(self, name:str):
        #----------------------------------------------#
        for object in self.objects.copy():
            #----------------------------------------------#
            if object.name == name:
                self.objects.remove(object)
#==============================================#
