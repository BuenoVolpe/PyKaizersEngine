#============================================================#
from engine.configs import configs
from engine.utils.log import printlog
#============================================================#
#type@namespace::context$path::extra?par1=v&par2=v2&#teporary_par=v3
#texture@pyk::characters.player$idle::white?scale=0.9&color='blue'&#enabled='false'
#------------------------------------------------------------#
seps = configs.engine.resource_strings_seps
#------------------------------------------------------------#
class ResourceReference:
    #------------------------------------------------------------#
    def __init__(self, resource_string:str,
            type:str, namespace:str, path:str, context:str=None,
            extra:str=None, parameters:dict={}, overrides:dict={}):
        #------------------------------------------------------------#
        self.resource_string:str = resource_string
        self.type:str=type
        self.namespace:str=namespace
        self.context:str=context
        self.path:str=path
        self.extra:str=extra
        self.parameters:dict=parameters
        self.overrides:dict=overrides
    #------------------------------------------------------------#
    def get_string(self) -> dict:
        return {
            "resource_string":self.resource_string,
            'type':self.type,
            'namespace':self.namespace,
            'context':self.context,
            'path':self.path,
            'extra':self.extra,
            'parameters':self.parameters,
            'overrides':self.overrides,
            }
    #------------------------------------------------------------#
    def log_items(self):
        printlog.dict(
            dict_name=self.resource_string,        
            dict={
            'type':self.type,
            'namespace':self.namespace,
            'context':self.context,
            'path':self.path,
            'extra':self.extra,
            'parameters':self.parameters,
            'overrides':self.overrides,
            },
            value_color="white",
        )
#------------------------------------------------------------#

