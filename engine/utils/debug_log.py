from engine.configs import configs
from typing import Any
#----------------------------------------------#
from game.enums.assetsmarks import assetsmarks
#----------------------------------------------#
from engine.utils.log import log, log_error, log_list, log_dict, log_success
from engine.utils.dict_to_class import dict_to_class
#==============================================#
class DebugLog:
    #==============================================#
    def handle_degub_string(self, debug_string:str) -> object:
        #================================#
        debug_string_concatenated = debug_string.split("::")
        #--------------------------------#
        debug_mark:str = debug_string_concatenated[0]
        if debug_mark not in [assetsmarks.engine.debug, assetsmarks.game.debug]:
            mark:str = debug_mark.split("@")[0]
            log_error(f"invalid debug string: {debug_string}, debug marker must be {configs.engine.asset_marks.debug} not {mark}")
            return
        #--------------------------------#
        if len(debug_string_concatenated) != 2:
            log_error(f"invalid debug string: {debug_string}, debug string must have oly 2 separetors")
            return
        debug_path:str = debug_string_concatenated[1]
        #--------------------------------#
        full_name:str = debug_path.split(".")
        if len(full_name) != 2:
            log_error(f"invalid debug string: {debug_string}, debug string must have only 2 paths parts")
            return
        #--------------------------------#
        obj, name = full_name
        return dict_to_class({
            "obj": obj,
            "name":name,
            "full_name": full_name
        })
    #==============================================#
    def get_metadata(self, debug_metadata:object, debug_string_info:object) -> object:
        #--------------------------------#
        if not debug_string_info: return
        #--------------------------------#
        obj_data:dict = debug_metadata.get(debug_string_info.obj, {})
        #--------------------------------#
        if not obj_data:
            log_error(f"cant find object in {debug_string_info.full_name}")
            return
        #--------------------------------#
        debug_data:dict = obj_data.get(debug_string_info.name, {})
        if not debug_data:
            log_error(f"cant find debug data in {debug_string_info.full_name}")
            return
        #================================#
        if not debug_data.do_debug:
            return
        return debug_data
    #==============================================#
    def get_log_data(self, metadata:object, full_name:str, **kwargs) -> object:
        #----------------------------------------------#
        log_data = dict_to_class({})
        #----------------------------------------------#
        log_data.color = (metadata.get("color")
                            if kwargs.get("color") is None
                            else kwargs.get("color", "black"))
        log_data.styles = (metadata.get("styles")
                            if kwargs.get("styles") is None
                            else kwargs.get("styles", []))
        log_data.console = (metadata.get("console")
                            if kwargs.get("console") is None
                            else kwargs.get("console", None))
        log_data.list_name = (metadata.get("list_name")
                            if kwargs.get("list_name") is None
                            else kwargs.get("list_name", ""))
        log_data.list_color = (metadata.get("list_color")
                            if kwargs.get("list_color") is None
                            else kwargs.get("list_color", "white"))
        log_data.key_color = (metadata.get("key_color")
                            if kwargs.get("key_color") is None
                            else kwargs.get("key_color", "yellow"))
        log_data.value_color = (metadata.get("value_color")
                            if kwargs.get("value_color") is None
                            else kwargs.get("value_color", "white"))
        log_data.styles = (metadata.get("styles")
                            if kwargs.get("styles") is None
                            else kwargs.get("styles", []))
        log_data.list_styles = (metadata.get("list_styles")
                            if kwargs.get("list_styles") is None
                            else kwargs.get("list_styles", []))
        log_data.dict_name = (metadata.get("dict_name")
                            if kwargs.get("dict_name") is None
                            else kwargs.get("dict_name", ""))
        log_data.name_color = (metadata.get("name_color")
                            if kwargs.get("name_color") is None
                            else kwargs.get("name_color", "white"))
        log_data.name_styles = (metadata.get("name_styles")
                            if kwargs.get("name_styles") is None
                            else kwargs.get("name_styles", []))
        log_data.name_in_overlay = (metadata.get("name_in_overlay",
                            full_name) if kwargs.get("name_in_overlay")
                            is None else kwargs.get("name_in_overlay", full_name))
        #----------------------------------------------#
        return log_data
    #==============================================#
    class DebugValue:
        #----------------------------------------------#
        value:str
        color:str
        category:str
        #----------------------------------------------#
        order:int = 0
        # formatter = None
        history:bool = False
    #==============================================#
    def log(self, debug_string:str, value:Any, **kwargs):
        #----------------------------------------------#
        # kwargs = dict_to_class(kwargs) or dict_to_class({})
        #----------------------------------------------#
        debug_metadata = configs.debug 
        debug_string_info = self.handle_degub_string(debug_string)
        #----------------------------------------------#
        data = self.get_metadata(debug_metadata, debug_string_info)
        if not data: return
        #----------------------------------------------#
        log_data = self.get_log_data(debug_metadata, debug_string_info.full_name, **kwargs)
        #==============================================#
        match data.log_type:
            #----------------------------------------------#
            case "log":
                log(value,
                log_data.color, 
                log_data.styles, 
                log_data.console)
            #----------------------------------------------#
            case "list":
                log_list(value,
                log_data.color, 
                log_data.styles, 
                log_data.list_name, 
                log_data.list_color, 
                log_data.list_styles, 
                log_data.console)
            #----------------------------------------------#
            case "error":
                log_error(value,
                log_data.console)
            #----------------------------------------------#
            case "dict":
                log_dict(value,
                log_data.key_color, 
                log_data.value_color, 
                log_data.styles, 
                log_data.dict_name, 
                log_data.name_color, 
                log_data.name_styles, 
                log_data.console)
            #----------------------------------------------#
            case "succes":
                log_success(value,
                log_data.console)
            #----------------------------------------------#
            case "overlay":
            #----------------------------------------------#
                data = self.DebugValue(
                    value=value,
                    color=log_data.color,
                    category=log_data.category,
                    order=debug_metadata.get("order",0),
                    formatter=debug_metadata.get("formatter",None)
                )
            
        
#==============================================#
debug_log:DebugLog = DebugLog()
#==============================================#

