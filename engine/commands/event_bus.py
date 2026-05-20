from engine.console import command, console
from engine.configs.settings import settings
#--------------------------------#
from engine.utils.log import log, log_success, log_error
from engine.utils.event_bus import event_bus
from engine.console.ui.surface import ConsoleSurface
#================================#
@command("event.emit", protection_level=2)
def event_emit(name, **data):
    """emits a event"""
    #--------------------------------#
    event_bus.emit(name, **data)
    return f"event {name} emited with data {data}"

@command("event.debug", protection_level=0)
def event_debug(do_debug=None):
    """chane a key fro value from settings"""
    #--------------------------------#
    if do_debug is None:
        event_bus.debug = not event_bus.debug
    else:
        event_bus.debug = do_debug
    return f"event debpuration set to {do_debug}"
