#============================================================#
from engine.configs import configs
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
#============================================================#
from engine.resource_string.resource_reference import ResourceReference
from engine.resource_string.parser.value import ResourceStringValueParser
#============================================================#
class ResourceStringParameters:
    #============================================================#
    def __init__(self, separators, value_parser=None):
        #------------------------------------------------------------#
        self.seps = separators
        #------------------------------------------------------------#
        self.value_parser = (
            value_parser
            or ResourceStringValueParser()
        )
    #============================================================#
    def parse(self, parameter_string: str) -> dict:
        #------------------------------------------------------------#
        parameters = {}
        #------------------------------------------------------------#
        if not parameter_string:
            return parameters
        #------------------------------------------------------------#
        for parameter in parameter_string.split(
            self.seps.parameters_split
        ):
            #------------------------------------------------------------#
            parameter = parameter.strip()
            #------------------------------------------------------------#
            if not parameter:
                continue
            #------------------------------------------------------------#
            if self.seps.parameters_setter not in parameter:
                printlog.error(
                    f"invalid resource parameter: {parameter}"
                )
                continue
            #------------------------------------------------------------#
            name, value = parameter.split(
                self.seps.parameters_setter,
                1
            )
            #------------------------------------------------------------#
            name = name.strip()
            #------------------------------------------------------------#
            if not name:
                #------------------------------------------------------------#
                printlog.error(
                    f"invalid resource parameter name: {parameter}"
                )
                continue
            #------------------------------------------------------------#
            parameters[name] = self.value_parser.parse(value)
        #------------------------------------------------------------#
        return parameters
#============================================================#

    