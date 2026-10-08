from typing import Any
#============================================================#
from engine.configs import configs
from engine.utils.log import printlog
#------------------------------------------------------------#
from engine.utils.dict_to_class import dict_to_class
from engine.utils.build_origin import _build_origin
from game.globalclasses import globalclasses
#============================================================#
from engine.resource_string.resource_reference import ResourceReference
from engine.signalbus.listener import SignalListener
#============================================================#
seps = configs.engine.resource_strings_seps
#============================================================#
class Subscription:
    #============================================================#
    def __init__(self, bus):
        self.bus = bus
    #============================================================#
    def subscribe(self, signal: str,
                  function, origin=None, order: int = 9999,
                  once: bool = False, enabled: bool = True):
        #------------------------------------------------------------#
        if origin is None:
            origin = _build_origin(function)
        #------------------------------------------------------------#
        resource:ResourceReference = globalclasses.resource_string_manager.parse(signal)
        #------------------------------------------------------------#
        listener: SignalListener = SignalListener(
            function=function,
            order=order,
            origin=origin,
            once=once,
            enabled=enabled,
            brute_ctxt_data=resource.parameters,
        )
        #------------------------------------------------------------#
        if resource.string not in self.bus.listeners:
            self.bus.listeners[resource.string] = []
        self.bus.listeners[resource.string].append(listener)
        #------------------------------------------------------------#
        signalfunc = self._create_signalfunc_string(
            globalclasses.resource_string_manager.parse(resource.string),
            origin
        )
        #------------------------------------------------------------#
        self.bus.listeners_atlas[signalfunc] = listener
        return listener
    #============================================================#
    def unsubscribe(self, string: SignalListener | str):
        #------------------------------------------------------------#
        if isinstance(string, str):
            refence:ResourceReference = globalclasses.resource_string_manager.parse(string)
            if refence.type == configs.engine.resource_type_marks.signal:
                return self.unsubscribe_signal(string)
            elif refence.type == configs.engine.resource_type_marks.signallistener:
                return self.unsubscribe_string(string)
            #------------------------------------------------------------#
            printlog.error(
                f"{string} is not a valid resource string"
            )
            #------------------------------------------------------------#
            return None
        #------------------------------------------------------------#
        elif isinstance(string, SignalListener):
            return self.unsubscribe_listener(string)
        #------------------------------------------------------------#
        else:
            printlog.error(
                f"{string} is not a valid listener neither a valid resource string"
            )
            return None
    #============================================================#
    def unsubscribe_signal(self, string: str):
        #------------------------------------------------------------#
        if string not in self.bus.listeners:
            printlog.error(
                f"signal {string} is not registered"
            )
            return False

        #------------------------------------------------------------#
        listeners = self.bus.listeners.pop(string)
        #------------------------------------------------------------#
        # Remove listeners
        for resource_string, listener in self.bus.listeners_atlas.copy().items():
            if listener in listeners:
                self.bus.listeners_atlas.pop(resource_string)
        #------------------------------------------------------------#
        return True
    #============================================================#
    def unsubscribe_string(self, string: str):
        """
        Remove a listener using resource string.
        """
        #------------------------------------------------------------#
        if string not in self.bus.listeners_atlas:
            printlog.error(
                f"resource {string} is not valid as a signal listener"
            )
            return False
        #------------------------------------------------------------#
        listener: SignalListener = self.bus.listeners_atlas[string]
        #------------------------------------------------------------#
        removed = self.unsubscribe_listener(listener)
        #------------------------------------------------------------#
        if removed:
            self.bus.listeners_atlas.pop(string, None)
        #------------------------------------------------------------#
        return removed
    #============================================================#
    def unsubscribe_listener(self, resource: SignalListener):
        """
        Remove a listener directally by its SignalListener object.
        """
        #------------------------------------------------------------#
        found = False
        #------------------------------------------------------------#
        for signal, listeners in self.bus.listeners.copy().items():
            if resource not in listeners:
                continue
            #--------------------------------------------------------#
            listeners.remove(resource)
            found = True
            #--------------------------------------------------------#
            if not listeners:
                self.bus.listeners.pop(signal, None)
            #--------------------------------------------------------#
            break
        #------------------------------------------------------------#
        if not found:
            printlog.error(
                f"listener {resource} is not registered"
            )
            return False
        #------------------------------------------------------------#
        for string, listener in self.bus.listeners_atlas.copy().items():
            if listener is resource:
                self.bus.listeners_atlas.pop(string, None)
        #------------------------------------------------------------#
        return True
    #============================================================#
    def _create_signalfunc_string(
        self,
        signal_reference: ResourceReference,
        origin: str
    ):
        #------------------------------------------------------------#
        origin = dict_to_class(origin)
        #------------------------------------------------------------#
        if origin.namespace == 'engine':
            namespace: str = configs.engine.acronym
        #------------------------------------------------------------#
        else:  # game
            #------------------------------------------------------------#
            if configs.game.engine_main_classes not in origin.qualname.split("."):
                namespace: str = configs.engine.acronym
            #--------------------------------------------------------#
            else:
                namespace: str = configs.game.acronym
        #============================================================#
        type: str = (
            f"{configs.engine.resource_type_marks.signallistener}"
            f"{seps.type}"
        )
        namespace: str = f"{namespace}{seps.namespace}"
        #------------------------------------------------------------#
        context: str = (
            f"{signal_reference.namespace}."
            f"{signal_reference.path}"
            f"{seps.context}"
        )
        #------------------------------------------------------------#
        path: str = f"{origin.qualname}"
        #------------------------------------------------------------#
        string: str = f"{type}{namespace}{context}{path.lower()}"
        return string
#============================================================#
# listener = subscription.subscribe(
#     "Signal@pyk::pyevent.key.down",
#     player.on_key_down
# )
#------------------------------------------------------------#
# subscription.unsubscribe(listener)
# subscription.unsubscribe(
#     "signalfunc@pyk::pyk.pyevent.key.down&game.player.on_key_down"
# )
# subscription.unsubscribe(
#     "signal@pyk::pyevent.key.down"
# )
    