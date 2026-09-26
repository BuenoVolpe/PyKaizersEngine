#============================================================#
from engine.configs import configs
#============================================================#
from engine.resources_string.resource_reference import ResourceReference
from engine.resources_string.parser import ResourceStringParser
#============================================================#
#type@namespace::context$path::extra?par1=v&par2=v2&#teporary_par=v3
#texture@pyk::characters.player$idle::white?scale=0.9&color='blue'&#enabled='false'
#------------------------------------------------------------#
class ResourceStringManager:
    #------------------------------------------------------------#
    def __init__(self):
        #------------------------------------------------------------#
        self.parser:ResourceStringParser = ResourceStringParser()
        #-------------------------------------------:-----------------#
    def parse(self, resource_string:str):
        return self.parser.parse(resource_string)
#------------------------------------------------------------#