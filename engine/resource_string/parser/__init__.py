from engine.configs import configs
from engine.utils.dict_to_class import dict_to_class
from engine.utils.log import printlog
#============================================================#
from engine.resource_string.resource_reference import ResourceReference
#------------------------------------------------------------#
from engine.resource_string.parser.validator import ResourceStringValidator
from engine.resource_string.parser.value import ResourceStringValueParser
from engine.resource_string.parser.tokenizer import ResourceStringTokenizer
from engine.resource_string.parser.parameters import ResourceStringParameters
from engine.resource_string.parser.structure import ResourceStringStructureParser
#============================================================#
class ResourceStringParser:
    #============================================================#
    def __init__(self):
        #============================================================#
        self.seps = configs.engine.resource_strings_seps
        #------------------------------------------------------------#
        self.validator:ResourceStringValidator = ResourceStringValidator(self.seps)
        self.tokenizer:ResourceStringTokenizer = ResourceStringTokenizer(self.seps)
        self.value_parser:ResourceStringValueParser = ResourceStringValueParser()
        self.parameters:ResourceStringParameters = ResourceStringParameters(self.seps)
        self.structure:ResourceStringStructureParser = ResourceStringStructureParser(self.seps)
    #============================================================#
    def parse(self, resource_string: str) -> ResourceReference | None:
        #------------------------------------------------------------#
        if not resource_string: return None
        #------------------------------------------------------------#
        context = dict_to_class(self.structure.parse(resource_string))
        resource_string, parameter_string, override_string = (
            self.tokenizer.separate_parameters(
                resource_string
            )
        )
        #------------------------------------------------------------#
        context.parameters = self.parameters.parse(parameter_string)
        context.overrides = self.parameters.parse(override_string)
        #------------------------------------------------------------#
        return ResourceReference(
            resource_string,
            type=context.type,
            namespace=context.namespace,
            context=context.context,
            path=context.path,
            extra=context.extra,
            parameters=context.parameters,
            temporary_parameters=context.overrides,
        )
    #============================================================#
