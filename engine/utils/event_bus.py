from engine.console import console
from engine.utils.log import log, log_error
from engine.configs.settings import settings
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
        self.debug = settings.get("event_bus_debug", False)
    #================================#
    def clear(self):
        #--------------------------------#
        self.listeners = {}
        self.queue = deque()
    #================================#
    def subscribe(self, event_name, callback, priority=0):
        #--------------------------------#
        if self.debug:
            log(f"[EVENT] Subscribed to {event_name} with priority {priority} -> {callback}", console=console)
        #--------------------------------#
        #Input>Gameplay>Sounds>UI>Debug
        self.listeners.setdefault(event_name, []).append((priority, callback))
        #--------------------------------#
        self.listeners[event_name].sort(key=lambda x: x[0])#, reverse=True)
    #================================#
    def unsubscribe(self, event_name, callback):
        #--------------------------------#
        if self.debug:
            log(f"[EVENT] Unsubscribed from {event_name} -> {callback}", console=console)
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
            log(f"[EVENT] Emitted {event_name} -> {data} to {self.listeners.get(event_name, [])[:]}", console=console)
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
                log(f"[EVENT] {event_name} -> {data} to {self.listeners.get(event_name, [])[:]}", console=console)
            #--------------------------------#
            for _, callback in self.listeners.get(event_name, [])[:]:
                if self.debug:
                    log(f"[EVENT] {event_name} -> {data} to {self.listeners.get(event_name, [])[:]}", console=console)
                #--------------------------------#
                if "data" in data:
                    #--------------------------------#
                    callback(data["entity"], **data["data"])
                    continue
                #--------------------------------#
                try:
                    callback(**data)
                except Exception as e:
                    log_error(f"Error on callback {callback}, with data {data}")
                    log_error(e)

                    
#================================#
event_bus = EventBus()



