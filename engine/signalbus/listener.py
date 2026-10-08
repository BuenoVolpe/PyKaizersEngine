#============================================================#
from engine.configs import configs
from engine.utils.log import printlog
#============================================================#
class SignalListener:
    def __init__(self, function, order:int, origin:str, once:bool=False, enabled:bool=True, brute_ctxt_data:dict={}):
        #------------------------------------------------------------#
        self.function = function
        self.order = order
        self.once = once
        self.origin = origin
        self.enabled = enabled

        self.resource_string:str

        self.brute_ctxt_data:dict = brute_ctxt_data
    #============================================================#
    def set_enabled(self, enabled:bool=None):
        #------------------------------------------------------------#
        if enabled is None:
            self.enabled:bool = not self.enabled
            return
        #------------------------------------------------------------#
        self.enabled:bool = enabled