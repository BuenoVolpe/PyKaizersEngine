

from typing import Any
#============================================================#
from engine.configs import configs
from engine.utils.dict_to_class import dict_to_class, GenericClass
from engine.resource_string.resource_reference import ResourceReference
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
        self.bus.queue.append((signal, ctxt))
    #============================================================#
    def _build_ctxt(self, signal: str, ctxt:object | dict, create_newctxt:bool=True) -> list[str, object]:
        #------------------------------------------------------------#
        resource:ResourceReference = globalclasses.resource_string_manager.parse(signal)
        #------------------------------------------------------------#
        newctxt = {}
        #------------------------------------------------------------#
        if isinstance(ctxt, GenericClass):
            ctxt = ctxt._data
        #------------------------------------------------------------#
        if create_newctxt:
            for key, value in ctxt.items():
                newctxt[key] = value
            for key, value in resource.temporary_parameters.items():
                newctxt[key] = value
            return resource.string, newctxt
        #------------------------------------------------------------#
        return resource, signal, ctxt
        #------------------------------------------------------------#
    #============================================================#
    def imadiate_emit(self, signal: str, ctxt:object | dict) -> list[Any]:
        #------------------------------------------------------------#
        resource, signal, ctxt = self._build_ctxt(signal, ctxt, create_newctxt=False)
        results:list = []
        #------------------------------------------------------------#
        for listener in self.bus.listeners.get(resource.string, [])[:]:
            #------------------------------------------------------------#
            self.bus.listeners[resource.string].sort(
                key=lambda listener: listener.order,
                reverse=False
            )
            #------------------------------------------------------------#
            result = None
            #------------------------------------------------------------#
            try:
                if not listener.enabled: continue
                #----------------------------------------------------------#
                send_ctxt:dict = {}
                for name, value in ctxt._data.items():
                    send_ctxt[name]=value
                for name, value in listener.brute_ctxt_data.items():
                    send_ctxt[name]=value
                for name, value in resource.temporary_parameters.items():
                    send_ctxt[name]=value
                #------------------------------------------------------------#
                listener.function(dict_to_class(send_ctxt))
                #------------------------------------------------------------#
                # listener.function(dict_to_class(ctxt))
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
            resource, signal, ctxt = self._build_ctxt(signal, ctxt, create_newctxt=False)
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
                    #----------------------------------------------------------#
                    send_ctxt:dict = {}
                    for name, value in ctxt._data.items():
                        send_ctxt[name]=value
                    for name, value in listener.brute_ctxt_data.items():
                        send_ctxt[name]=value
                    for name, value in resource.temporary_parameters.items():
                        send_ctxt[name]=value
                    #------------------------------------------------------------#
                    listener.function(dict_to_class(send_ctxt))
                    #------------------------------------------------------------#
                    # listener.function(dict_to_class(ctxt))
                #------------------------------------------------------------#
                except Exception as e:
                    printlog.error(
                        f"Error on callback {listener.origin.file} ({listener.origin.line}), "
                        f"with data {ctxt._data}"
                    )
                    printlog.error(e)