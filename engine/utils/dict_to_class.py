def dict_to_class(data):
    #--------------------------------#
    obj = GenericClass()
    #--------------------------------#
    for key, value in data.items():
        #--------------------------------#
        if isinstance(value, dict):
            #--------------------------------#
            if value.get("subclass", False):
                value = dict_to_class(value)
                continue
        #--------------------------------#
        setattr(obj, key, value)
    #=====================================#
    obj._data = data
    #--------------------------------#
    return obj

#=====================================#
class GenericClass:
    ...

