from engine.signalbus import signalbus
from engine.utils.build_origin import _build_origin
#============================================================#
def subscribe(signal: str = "None", order:int=9999, once:bool=False, enabled:bool=True):
    #------------------------------------------------------------#
    def decorator(func):
        func.__signal__ = signal
        #------------------------------------------------------------#
        return func, signalbus.subscribe(signal, func, _build_origin(func), order, once, enabled)
    #------------------------------------------------------------#
    return decorator
