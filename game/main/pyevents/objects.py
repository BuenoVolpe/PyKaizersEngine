#==============================================#
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
from engine.utils.sort_list import sort_objects
#==============================================#
class Objects:
    #==============================================#
    def __init__(self):
        #----------------------------------------------#
        self.objects:list[dict] = [] #{"object":object, "name":name, "order":num}
    #==============================================#
    def add_object(self, obj:object, name:str=None, order:int=None):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            if order is None:
                order:int = 999 
            #----------------------------------------------#
            if name is None:
                name:str = f"{obj.__class__.__name__}.{time.time()}"
            #----------------------------------------------#
            obj_:object = dict_to_class({"object":obj, "name":name, "order":order})
            self.objects.append(obj_)
            self.objects:list = sort_objects(self.objects)
            #----------------------------------------------#
            printlog.success(f"object {name} was added from event_handler's objects")
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"object cannot add {name} from event_handler's objects; \n {e}")
    #==============================================#
    def remove_object(self, name:str):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            for object in self.objects.copy():
                #----------------------------------------------#
                if object.name == name:
                    self.objects.remove(object)
                printlog.success(f"object {name} was removed from event_handler's objects")
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"object cannot remove {name} from event_handler's objects; \n {e}")
