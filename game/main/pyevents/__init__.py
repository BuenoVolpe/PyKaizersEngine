import pygame as pg
from sys import exit
from typing import Any
#============================================================#
from engine.signalbus import signalbus
from game.enums.signals import signals
from game.enums.signals_order import signals_order
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
        #------------------------------------------------------------#
        signalbus.subscribe(signals.EVENT_HANDLER_ADD_OBJECT, self.add_object, order=signals_order.ADDOBJ)
        signalbus.subscribe(signals.EVENT_HANDLER_REMOVE_OBJECT, self.remove_object, order=signals_order.REMOVEOBJ)
    #============================================================#
    def quit(self, event:pg.event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_LALT):
            #------------------------------------------------------------#
            pg.quit()
            exit()
    #============================================================#
    def handle(self, delta_time:int) -> dict:
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
                signalbus.emit(signals.KEYDOWN, {'pyevent':event, "delta_time":delta_time})
                result:Any = handle_KEYDOWN(event)
            #------------------------------------------------------------#
            elif event.type == pg.KEYUP:
                signalbus.emit(signals.KEYUP, {'pyevent':event, "delta_time":delta_time})
                result:Any = handle_KEYUP(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEBUTTONDOWN:
                signalbus.emit(signals.MOUSEBUTTONDOWN, {'pyevent':event, "delta_time":delta_time})
                result:Any = handle_MOUSEBUTTONDOWN(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEBUTTONUP:
                signalbus.emit(signals.MOUSEBUTTONUP, {'pyevent':event, "delta_time":delta_time})
                result:Any = handle_MOUSEBUTTONUP(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEMOTION:
                signalbus.emit(signals.MOUSEMOTION, {'pyevent':event, "delta_time":delta_time})
                result:Any = handle_MOUSEMOTION(event)
            #------------------------------------------------------------#
            elif event.type == pg.MOUSEWHEEL:
                signalbus.emit(signals.MOUSEWHEEL, {'pyevent':event, "delta_time":delta_time})
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