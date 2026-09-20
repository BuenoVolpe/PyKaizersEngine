import pygame as pg
from sys import exit
from typing import Any
#==============================================#
from engine.utils.log import printlog
from engine.signal_bus import signal_bus
from game.enums.signals import signals
#==============================================#
def handle_event_KEYDOWN(event: pg.event) -> Any:
    #----------------------------------------------#
    result = None
    #----------------------------------------------#
    signal_bus.emit(signals.PGEVENT_KEY_DOWN, event=event)
    #==============================================#
    #events
    #==============================================#
    return result 
#==============================================#