class ResourceStringTokenizer:
    #============================================================#
    def __init__(self, separators):
        #------------------------------------------------------------#
        self.seps = separators
    #============================================================#
    def separate_parameters(self, resource_string: str):
        #------------------------------------------------------------#
        if self.seps.parameters not in resource_string:
            return resource_string, None, None
        #------------------------------------------------------------#
        resource_string, parameter_string = resource_string.split(
            self.seps.parameters,
            1
        )
        #------------------------------------------------------------#
        normal = None
        temporary = None
        #------------------------------------------------------------#
        if self.seps.temporary_parameters in parameter_string:
            #------------------------------------------------------------#
            normal, temporary = parameter_string.split(
                self.seps.temporary_parameters,
                1
            )
        #------------------------------------------------------------#
        else:
            normal = parameter_string
        #------------------------------------------------------------#
        return resource_string, normal, temporary
#============================================================#

