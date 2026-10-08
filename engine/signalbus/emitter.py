

from typing import Any
#============================================================#
from engine.configs import configs
from engine.utils.dict_to_class import dict_to_class
from engine.utils.log import printlog
from game.globalclasses import globalclasses
#============================================================#
seps = configs.engine.resource_strings_seps
#============================================================#
class SignalEmitter:
    #============================================================#
    def __init__(self, bus):
        self.bus = bus
    #============================================================#
    def emit(self, signal: str, ctxt:object | dict):
        #------------------------------------------------------------#
        # signal, ctxt = self.build_ctxt(signal, ctxt)
        #------------------------------------------------------------#
        self.bus.queue.append((signal, ctxt))
    #============================================================#
    def imadiate_emit(self, signal: str, ctxt:object | dict) -> list[Any]:
        #------------------------------------------------------------#
        # signal, ctxt = self.build_ctxt(signal, ctxt)
        results:list = []
        #------------------------------------------------------------#
        for listener in self.bus.listeners.get(signal, [])[:]:
            #------------------------------------------------------------#
            self.bus.listeners[signal].sort(
                key=lambda listener: listener.order,
                reverse=False
            )
            #------------------------------------------------------------#
            result = None
            #------------------------------------------------------------#
            try:
                if not listener.enabled: continue
                #----------------------------------------------------------#
                # send_ctxt:dict = {}
                # for name, value in ctxt._data.items():
                #     send_ctxt[name]=value
                # for name, value in listener.brute_ctxt_data.items():
                #     send_ctxt[name]=value--
                # #------------------------------------------------------------#
                # listener.function(dict_to_class(send_ctxt))
                # #------------------------------------------------------------#
                listener.function(dict_to_class(ctxt))
            except Exception as e:
                printlog.error(
                    f"Error on callback {listener.origin}, "
                    f"with data {ctxt._data}"
                )
                printlog.error(e)
            #------------------------------------------------------------#
            if result is not None:
                results.append(result)
        return result
    #============================================================#
    def process(self):
        while self.bus.queue:
            #------------------------------------------------------------#
            signal, ctxt = self.bus.queue.popleft()
            #------------------------------------------------------------#
            for listener in self.bus.listeners.get(signal, [])[:]:
                #------------------------------------------------------------#
                self.bus.listeners[signal].sort(
                    key=lambda listener: listener.order,
                    reverse=False
                )
                #------------------------------------------------------------#
                try:
                    if not listener.enabled: continue
                    #------------------------------------------------------------#
                    send_ctxt:dict = {}
                    for name, value in ctxt._data.items():
                        send_ctxt[name]=value
                    for name, value in listener.brute_ctxt_data.items():
                        send_ctxt[name]=value
                    #------------------------------------------------------------#
                    listener.function(dict_to_class(send_ctxt))
                #------------------------------------------------------------#
                except Exception as e:
                    printlog.error(
                        f"Error on callback {listener.origin.file} ({listener.origin.line}), "
                        f"with data {ctxt._data}"
                    )
                    printlog.error(e)