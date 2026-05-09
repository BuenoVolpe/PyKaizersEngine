import pygame as pg
from collections import deque
import weakref
#================================#
from engine.configs.settings import settings
# from engine.debug.console import console, command, parse_kv_args
from engine.utils.log import log, log_error
#--------------------------------#
from game.enums.events import Events as Ev
from game.enums.packet_type import PacketType
from game.server import network
#================================#
class EventBus:
    #================================#
    def __init__(self):
        #--------------------------------#
        self.listeners = {}  # event: [(priority, func_ref)]
        self.queue = deque()
        #--------------------------------#
        self.debug = False
        #--------------------------------#
        self.network = None
    #================================#
    def emit(self, event: str, **data):
        #--------------------------------#
        parts = event.split(".")
        #--------------------------------#
        for i in range(len(parts), 0, -1):
            #--------------------------------#
            sub_event = ".".join(parts[:i])
            self.queue.append((sub_event, data))
    #================================#
    def emit_now(self, event: str, **data):
        #--------------------------------#
        self._dispatch(event, data)
    #================================#
    def process(self):
        #--------------------------------#
        while self.queue:
            #--------------------------------#
            event, data = self.queue.popleft()
            #--------------------------------#
            self._dispatch(event, data)
    #================================#
    def _dispatch(self, event, data):
        #--------------------------------#
        listeners = self.listeners.get(event, [])
        #--------------------------------#
        data["_event"] = event
        #--------------------------------#
        if self.debug:
            #--------------------------------#
            log(f"[EVENT] {event} -> {data}")
        #--------------------------------#
        for priority, func_ref in listeners[:]:
            #--------------------------------#
            func = func_ref()
            #--------------------------------#
            if func is None:
                #--------------------------------#
                listeners.remove((priority, func_ref))
                #--------------------------------#
                continue
            #--------------------------------#
            try:
                #--------------------------------#
                func(**data)
            #--------------------------------#
            except Exception as e:
                log_error(f"[ERROR] {event} -> {func.__name__}: {e}")

    #================================#
    def connect(self, func, event: str, priority: int = 0):
        #--------------------------------#
        try:
            #--------------------------------#
            func_ref = weakref.WeakMethod(func)
        #--------------------------------#
        except:
            #--------------------------------#
            func_ref = weakref.ref(func)
            log_error(f"could not create weak reference for {func}, using strong reference instead")
        #--------------------------------#
        if event not in self.listeners:
            #--------------------------------#
            self.listeners[event] = []
        #--------------------------------#
        self.listeners[event].append((priority, func_ref))
        self.listeners[event].sort(key=lambda x: x[0])
    #================================#
    def disconnect(self, func, event: str):
        #--------------------------------#
        if event not in self.listeners:
            return
        #--------------------------------#
        to_remove = []
        #--------------------------------#
        for priority, func_ref in self.listeners[event]:
            #--------------------------------#
            if func_ref() == func:
                #--------------------------------#
                to_remove.append((priority, func_ref))
        #--------------------------------#
        for item in to_remove:
            self.listeners[event].remove(item)
    #================================#
    def clear(self):
        #--------------------------------#
        self.listeners.clear()
        self.queue.clear()
    #================================#
    def set_network(self, network):
        self.network = network
    #================================#
    def emit_remote(self, event: str, **data):

        if not self.network:
            return

        self.network.send({
            "event": event,
            "data": data
        }, packet_type=PacketType.EVENT)


#================================#
event_bus = EventBus()
#================================#
#decorator
def event(event, priority=0):
    def wrapper(func):
        event_bus.connect(func, event, priority)
        return func
    return wrapper
#================================#
#events
@event(Ev.EXEMPLE)
def exemple():
    log("called exemple")
#================================#

# @event("player.hit.critical")
# def crit_fx(**data):
#     print("CRITICAL HIT")

# @event("player.hit")
# def normal_hit(**data):
#     print("any hit")

# @event("player")
# def anything_player(**data):
#     print("player event")

# @event(NetEvent.PLAYER_MOVE)
# def on_player_move(player_id, left, right):
#     ...

# event_bus.emit_remote(
#     NetEvent.PLAYER_MOVE,
#     left=True,
#     right=False
# )
