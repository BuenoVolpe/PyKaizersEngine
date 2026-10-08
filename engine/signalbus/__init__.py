from typing import Any
#============================================================#
from engine.configs import configs
#------------------------------------------------------------#
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
from engine.utils.build_origin import _build_origin
from engine.resource_string.resource_reference import ResourceReference
# from game.globalclasses import globalclasses
#============================================================#
from engine.signalbus.listener import SignalListener
from engine.signalbus.emitter import SignalEmitter
from engine.signalbus.subscription import Subscription
#============================================================#
from collections import deque
#============================================================#
class SignalBus:
    def __init__(self):
        #------------------------------------------------------------#
        self.listeners:dict[str, list[SignalListener]] = {}  # signal: [SignalListener, ...]
        self.listeners_atlas:dict[str, SignalListener] = {}  # signallistener: SignalListener, ...]
        self.queue = deque()
        #------------------------------------------------------------#
        self._subscription:Subscription = Subscription(self)
        self._emitter:SignalEmitter = SignalEmitter(self)
    #============================================================#
    def clear(self):
        self.listeners = {}  # signal: [SignalListener, ...]
        self.listeners_atlas = {}  # signallistener: SignalListener, ...
        self.queue = deque()
        #------------------------------------------------------------#
    #============================================================#
    def subscribe(self, signal:str,
                  function, origin=None, order:int=9999,
                  once:bool=False, enabled:bool=True):
        #------------------------------------------------------------#
        return self._subscription.subscribe(signal, function, origin, order, once, enabled)
    #------------------------------------------------------------#
    def unsubscribe(self, string: SignalListener | str):
        return self._subscription.unsubscribe(string)
    #------------------------------------------------------------#
    def unsubscribe_signal(self, string: str):
        return self._subscription.unsubscribe_signal(string)
    #------------------------------------------------------------#
    def unsubscribe_string(self, string: str):
        return self._subscription.unsubscribe_string(string)
    #------------------------------------------------------------#
    def unsubscribe_listener(self, resource: SignalListener):
        return self._subscription.unsubscribe_listener(resource)
    #============================================================#
    def emit(self, signal:str, ctxt:object | dict):
        self._emitter.emit()
    def imadiate_emit(self, signal:str, ctxt:object | dict) -> list[Any]:
        return self._emitter.imadiate_emit(signal, ctxt)
    def process(self):
        return self._emitter.process()

#============================================================#
signalbus:SignalBus = SignalBus()

#============================================================#
# decorator

