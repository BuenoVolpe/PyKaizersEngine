import pygame as pg
from sys import exit
from typing import Any
#==============================================#
from engine.utils.log import printlog
from engine.signal_bus import signal_bus
from game.enums.signals import signals
#==============================================#
def handle_event_KEYUP(event: pg.event) -> Any:
    #----------------------------------------------#
    signal_bus.emit(signals.PGEVENT_KEY_UP, event=event)
    #----------------------------------------------#
    result = None
    #==============================================#
    #events
    #==============================================#
    return result 
#==============================================#
