import pygame as pg
from sys import exit
from typing import Any
#============================================================#
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
from engine.utils.sort_list import sort_objects
#============================================================#
from game.main.pyevents.objects import Objects
from game.main.pyevents.handle_pyevents import (
    handle_KEYDOWN, handle_KEYUP, handle_MOUSEBUTTONDOWN,
    handle_MOUSEBUTTONUP, handle_MOUSEMOTION, handle_MOUSEWHEEL
)
#============================================================#
class PyEvents:
    #------------------------------------------------------------#
    def __init__(self):
        #------------------------------------------------------------#
        self.objects:Objects = Objects()
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
        results:list = []
        #------------------------------------------------------------#
        for event in events:
            #------------------------------------------------------------#
            result = None
            #------------------------------------------------------------#
            self.quit(event)
            #------------------------------------------------------------#
            if event.type == pg.KEYDOWN:
                result:Any = handle_KEYDOWN(event)
            #------------------------------------------------------------#
            elif event.type == pg.KEYUP:
                result:Any = handle_KEYUP(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEBUTTONDOWN:
                result:Any = handle_MOUSEBUTTONDOWN(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEBUTTONUP:
                result:Any = handle_MOUSEBUTTONUP(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEMOTION:
                result:Any = handle_MOUSEMOTION(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEWHEEL:
                result:Any = handle_MOUSEWHEEL(event)
            #------------------------------------------------------------#
            for obj in self.objects.objects:
                if hasattr("pyevents"):
                    obj.pyevents(event)
                if hasattr("pyevents_handler"):
                    obj.pyevents_handler(event)
                if hasattr("handle_pyevents"):
                    obj.handle_pyevents(event)
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
    def add_object(self, ctxt:object):
        return self.objects.add_object(ctxt.obj, ctxt.name, ctxt.order)
    #==============================================#
    def remove_object(self, ctxt:object):
        return self.objects.remove_object(ctxt.name)
#============================================================#