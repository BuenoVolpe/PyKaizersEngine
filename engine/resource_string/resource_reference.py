class ResourceReference:
    def __init__(self, resource_string:str,
                 type:str, namespace:str, path:str, context:str="", string:str=None,
                 extra:list=[], parameters:dict={}, temporary_parameters:dict={},):
        #-------------------------------------#
        self.type:str = type
        self.namespace:str = namespace
        self.context:str = context
        self.path:str = path
        #-------------------------------------#
        self.extra:list = extra
        self.parameters:dict = parameters
        self.temporary_parameters:dict = temporary_parameters
        #-------------------------------------#
        self.resource_string:str = resource_string
        self.string:str = string or resource_string
    