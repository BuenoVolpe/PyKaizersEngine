#============================================================#
from engine.configs import configs
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
#============================================================#
from engine.resources_string.resource_reference import ResourceReference
#============================================================#
#type@namespace::context$path::extra?par1=v&par2=v2&#teporary_par=v3
#texture@pyk::characters.player$idle::white?scale=0.9&color='blue'&#enabled='false'
#------------------------------------------------------------#
seps = dict_to_class(configs.engine.resource_strings_seps)
#------------------------------------------------------------#
class ResourceStringParser:
    #============================================================#
    def __init__(self):
        ...
    #============================================================#
    def parse(self, resource_string:str) -> ResourceReference | None:
        #------------------------------------------------------------#
        if not self._verify_string(resource_string): return
        #============================================================#
        original_resource_string:str = resource_string
        #============================================================#
        #temporary parameters
        temporary_parameters:dict = {}
        #------------------------------------------------------------#
        if seps.temporary_parameters in resource_string:
            #------------------------------------------------------------#
            resource_string, temporary_string = resource_string.split(seps.temporary_parameters, 1)
            #------------------------------------------------------------#
            temporary_parameters:dict = self._parse_parameters(
                temporary_string
            )
        #============================================================#
        #normal parameters
        parameters:dict = {}
        #------------------------------------------------------------#
        if seps.parameters in resource_string:
            #------------------------------------------------------------#
            resource_string, parameter_string = resource_string.split(seps.parameters, 1)
            #------------------------------------------------------------#
            parameters:dict = self._parse_parameters(
                parameter_string
            )
        #============================================================#
        #asset type
        if seps.type not in resource_string:
            printlog.error(f"resource_string {resource_string} must have an {seps.type} to define its type")
            return
        #------------------------------------------------------------#
        resource_type, resource_string = resource_string.split(seps.type)
        #============================================================#
        #namespace
        if seps.namespace not in resource_string:
            printlog.error(f"resource_string {resource_string} must have an {seps.namespace} to define its namespace")
            return
        #------------------------------------------------------------#
        namespace, resource_string = resource_string.split(seps.namespace, 1)
        #============================================================#
        #context
        context:str = None
        if seps.context in resource_string:
            context, resource_string = resource_string.split(seps.context)
        #============================================================#
        #extra & path
        extra:str = None
        path:str = resource_string
        if seps.extra in resource_string:
            path, extra = resource_string.split(seps.extra)
        #============================================================#
        return ResourceReference(
            resource_string=original_resource_string,
            type=resource_type,
            namespace=namespace,
            path=path,
            context=context,
            extra=extra,
            parameters=parameters,
            overrides=temporary_parameters
        )
            
    #------------------------------------------------------------#
    def _parse_parameters(self, parameter_string:str) -> dict:
        #------------------------------------------------------------#
        parameters = {}
        #------------------------------------------------------------#
        if not parameter_string: return parameters
        #------------------------------------------------------------#
        for parameter in parameter_string.split(seps.parameters_split):
            #------------------------------------------------------------#
            if not parameter:
                continue
            #------------------------------------------------------------#
            if seps.parameters_setter not in parameter:
                printlog.error(f"invalid resource parameter: {parameter}")
                continue
            #------------------------------------------------------------#
            name, value = parameter.split("=", 1)
            #------------------------------------------------------------#
            parameters[name] = self._parse_value(value)
        #------------------------------------------------------------#
    #============================================================#
    def _parse_value(self, value: str):
        #------------------------------------------------------------#
        value = value.strip()
        #============================================================#
        #strings
        if (len(value) >= 2 and value[0] == "'" and value[-1] == "'"):
            return value[1:-1]
        #------------------------------------------------------------#
        if (len(value) >= 2 and value[0] == '"' and value[-1] == '"'):
            return value[1:-1]
        #============================================================#
        if value.lower() in ["true", "t"]:
            return True
        if value.lower() in ["false", "f"]:
            return False
        #============================================================#
        # None
        if value.lower() in ["none", 'null']:
            return None
        #============================================================#
        #number
        try:
            #------------------------------------------------------------#
            if "." in value:
                return float(value)
            #------------------------------------------------------------#
            return int(value)
        #------------------------------------------------------------#
        except ValueError:
            pass
        #============================================================#
        #strings without quotation marks
        return value
    #============================================================#
    def _verify_string(self, resource_string:str) -> bool:
        #------------------------------------------------------------#
        if not isinstance(resource_string, str):
            printlog.error("resource string must be a string!")
            return False
        #------------------------------------------------------------#
        if not resource_string:
            printlog.error("resource string is empty!")
            return False
        #------------------------------------------------------------#
        if resource_string.find("@") == -1 or resource_string.find("::") == -1:
            printlog.error(f"resource string {resource_string} is invalid!")
            return False
        #------------------------------------------------------------#
        return True
    #============================================================#
