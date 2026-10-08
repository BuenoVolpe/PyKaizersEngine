import pygame as pg
import time
#==============================================#
from engine.utils.sort_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
from engine.utils.log import printlog
from engine.configs import configs
#============================================================#
from engine.signalbus import signalbus
from game.enums.signals import signals
from game.enums.signals_order import signals_order as sigorder
#============================================================#
from game.main.updater.objects import Objects
#==============================================#
class Updater:
    #==============================================#
    def __init__(self):
        #----------z------------------------------------#
        self.objects:Objects = Objects
        #----------z------------------------------------#
        signalbus.subscribe(signals.UPDATER_ADD_OBJECT, self.add_object, order=sigorder.ADDOBJ.FIRST)
        signalbus.subscribe(signals.UPDATER_REMOVE_OBJECT, self.remove_object, order=sigorder.REMOVEOBJ.FIRST)
    #==============================================#
    def update(self, delta_time:float):
        signalbus.emit(f"{signals.ENGINE_UPDATE}", ctxt={"delta_time":delta_time})
        #----------------------------------------------#
        ...
        #----------------------------------------------#
        signalbus.process()
        #----------------------------------------------#
    #==============================================#
    def add_object(self, ctxt:object):
        #----------------------------------------------#
        return self.objects.add_object(ctxt.object, ctxt.name, ctxt.order)
    #----------------------------------------------#
    def remove_object(self, ctxt:object):
        #----------------------------------------------#
        return self.objects.remove_object(ctxt.name)