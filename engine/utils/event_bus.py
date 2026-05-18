from engine.console import console
from engine.utils.log import log
#================================#
from collections import deque
#================================#
class EventBus:
    #================================#
    def __init__(self):
        #--------------------------------#
        self.listeners = {} #event_name: [(priority, callback)]
        self.queue = deque()
        #--------------------------------#
        self.debug = False
    #================================#
    def clear(self):
        #--------------------------------#
        self.listeners = {}
        self.queue = deque()
    #================================#
    def subscribe(self, event_name, callback, priority=0):
        #--------------------------------#
        if self.debug:
            log(f"[EVENT] Subscribed to {event_name} with priority {priority} -> {callback}", console)
        #--------------------------------#
        #Input>Gameplay>Sounds>UI>Debug
        self.listeners.setdefault(event_name, []).append((priority, callback))
        #--------------------------------#
        self.listeners[event_name].sort(key=lambda x: x[0])#, reverse=True)
    #================================#
    def unsubscribe(self, event_name, callback):
        #--------------------------------#
        if self.debug:
            log(f"[EVENT] Unsubscribed from {event_name} -> {callback}", console)
        #--------------------------------#
        if event_name in self.listeners:
            #--------------------------------#
            self.listeners[event_name] = [
                (p, cb) for p, cb in self.listeners[event_name]
                if cb != callback
            ]
    #================================#
    def emit(self, event_name, **data):
        #--------------------------------#
        if self.debug:
            log(f"[EVENT] Emitted {event_name} -> {data} to {self.listeners.get(event_name, [])[:]}", console)
        #--------------------------------# 
        self.queue.append((event_name, data))
    #================================#
    def process(self):
        #--------------------------------#
        while self.queue:
            #--------------------------------#
            event_name, data = self.queue.popleft()
            #--------------------------------#
            if self.debug:
                log(f"[EVENT] {event_name} -> {data} to {self.listeners.get(event_name, [])[:]}", console)
            #--------------------------------#
            for _, callback in self.listeners.get(event_name, [])[:]:
                #--------------------------------#
                if "data" in data:
                    #--------------------------------#
                    callback(data["entity"], **data["data"])
                    continue
                #--------------------------------#
                callback(**data)
#================================#
event_bus = EventBus()



