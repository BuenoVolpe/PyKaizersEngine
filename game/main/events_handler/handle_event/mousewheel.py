import pygame as pg
from sys import exit
from typing import Any
#==============================================#
from engine.utils.log import printlog
from engine.signal_bus import signal_bus
from game.enums.signals import signals
#==============================================#
def handle_event_MOUSEWHEEL(event: pg.event) -> Any:
    #----------------------------------------------#
    signal_bus.emit(signals.PGEVENT_MOUSE_WHEEL, event=event)
    #----------------------------------------------#
    result = None
    #==============================================#
    #events
    if event.y > 0:
        signal_bus.emit(signals.PGEVENT_MOUSE_WHEEL_UP, event=event)
    elif event.y < 0:
        signal_bus.emit(signals.PGEVENT_MOUSE_WHEEL_DOWN, event=event)
    #==============================================#
    return result 
#==============================================#
