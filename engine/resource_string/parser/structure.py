from engine.utils.log import printlog
#============================================================#
class ResourceStringStructureParser:
    def __init__(self, separators):
        self.seps = separators
    #============================================================#
    def parse(self, resource_string: str) -> dict | None:
        #------------------------------------------------------------#
        original = resource_string
        #============================================================#
        # "type@pyk::context$path!extra?par='value'&#temppar='value2'"
        #------------------------------------------------------------#
        result = {
            "type": None,
            "namespace": None,
            "context": None,
            "path": None,
            "extra": None,
            "parameters_string": None,
        }
        #============================================================#
        # type
        if self.seps.type not in resource_string:
            printlog.error(
                f"resource string must have "
                f"an {self.seps.type} to define its type"
            )
        #------------------------------------------------------------#
        resource_type, resource_string = resource_string.split(
            self.seps.type,
            1
        )
        #------------------------------------------------------------#
        result["type"] = resource_type
        #------------------------------------------------------------#
        # namespace
        if self.seps.namespace not in resource_string:
            #------------------------------------------------------------#
            printlog.error(
                f"resource string must have "
                f"an {self.seps.namespace} to define its namespace"
            )
        #------------------------------------------------------------#
        namespace, resource_string = resource_string.split(
            self.seps.namespace,
            1
        )
        #------------------------------------------------------------#
        result["namespace"] = namespace
        #------------------------------------------------------------#
        # context
        if self.seps.context in resource_string:
            #------------------------------------------------------------#
            context, resource_string = resource_string.split(
                self.seps.context,
                1
            )
            #------------------------------------------------------------#
            result["context"] = context
        #------------------------------------------------------------#
        # extra
        if self.seps.extra in resource_string:
            #------------------------------------------------------------#
            path, extra = resource_string.split(
                self.seps.extra,
                1
            )
            #------------------------------------------------------------#
            result["path"] = path
            #------------------------------------------------------------#
            #parameters
            if self.seps.parameters in extra:
                extra, parameters_string = resource_string.split(
                    self.seps.parameters, 1 
                )
                #------------------------------------------------------------#
                result["parameters_string"] = parameters_string
            #------------------------------------------------------------#
            result["extra"] = extra
        #------------------------------------------------------------#
        else:
            result["path"] = resource_string
        #------------------------------------------------------------#
        return result

    
