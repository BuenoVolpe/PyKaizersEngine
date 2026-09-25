from pathlib import Path
#============================================================#
from engine.utils.json import json_reader, json_writer
from engine.utils.log import log, log_success
#============================================================#
class ConfigsBase:

    def __init__(self, path: str | dict = "assets/config/settings.json"):
        #------------------------------------------------------------#
        if isinstance(path, dict):
            self._path = None
            self._data = path.copy()
        #------------------------------------------------------------#
        else:
            self._path = Path(path)
            self._data = json_reader(path, {})
        #------------------------------------------------------------#
        # Carrega o default antes do config do usuário
        self._load_default()
        #------------------------------------------------------------#
        self.set_dynamically_settings(self._data)
        self.set_essential_values()
    #============================================================#
    def _load_default(self):
        #------------------------------------------------------------#
        default_path = self._data.get("default_path")
        #------------------------------------------------------------#
        if not default_path:
            return
        #------------------------------------------------------------#
        default_data = json_reader(default_path, {})
        self._default_path = Path(default_path)
        #------------------------------------------------------------#
        self._data = self._merge(
            default_data,
            self._data
        )
    #============================================================#
    @staticmethod
    def _merge(base: dict, override: dict) -> dict:
        #------------------------------------------------------------#
        result = base.copy()
        #------------------------------------------------------------#
        for key, value in override.items():
            #------------------------------------------------------------#
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                #------------------------------------------------------------#
                result[key] = ConfigsBase._merge(
                    result[key],
                    value
                )
            #------------------------------------------------------------#
            else:
                result[key] = value
        #------------------------------------------------------------#
        return result
    #============================================================#
    def set_essential_values(self):
        ...
    #============================================================#
    def set_to_default(self):
        #------------------------------------------------------------#
        default_path = self._data.get("default_path")
        #------------------------------------------------------------#
        if not default_path:
            return
        #------------------------------------------------------------#
        default_data = json_reader(default_path, {})
        #------------------------------------------------------------#
        self._data = default_data.copy()
        #------------------------------------------------------------#
        self.set_dynamically_settings(self._data)
        self.set_essential_values()
        #------------------------------------------------------------#
        log_success(
            f"{self.__class__.__name__} set to default"
        )
    #============================================================#
    def get_path(self, path: str):
        #------------------------------------------------------------#
        node = self
        #------------------------------------------------------------#
        for key in path.split("."):
            #------------------------------------------------------------#
            if not hasattr(node, key):
                return None
            #------------------------------------------------------------#
            node = getattr(node, key)
        #------------------------------------------------------------#
        return node
    #============================================================#
    def create_subclass(self, data: dict, name: str):
        #------------------------------------------------------------#
        subclass = ConfigsBase(data)
        #------------------------------------------------------------#
        setattr(self, name, subclass)
    #============================================================#
    def set_dynamically_settings(self, data: dict):
        #------------------------------------------------------------#
        for key, value in data.items():
            #------------------------------------------------------------#
            if isinstance(value, dict):
                #------------------------------------------------------------#
                if value.get("subclass", False):
                    self.create_subclass(value, key)
                    continue
            #------------------------------------------------------------#
            setattr(self, key, value)
        #------------------------------------------------------------#
        if not hasattr(self, "_data"):
            self._data = data
    #============================================================#
    def get(self, key: str, default=None):
        #------------------------------------------------------------#
        if hasattr(self, key):
            return getattr(self, key)
        #------------------------------------------------------------#
        return default
    #============================================================#
    def set(self, key: str, value=None):
        #------------------------------------------------------------#
        if callable(getattr(self, key, None)):
            raise ValueError(
                f"Cannot overwrite method '{key}'"
            )
        #------------------------------------------------------------#
        setattr(self, key, value)
        #------------------------------------------------------------#
        self._data[key] = value
        #------------------------------------------------------------#
        self.save()
    #============================================================#
    def save(self):
        #------------------------------------------------------------#
        json_writer(
            self._path,
            self._data
        )
        #------------------------------------------------------------#
        log_success(
            f"{self.__class__.__name__} saved: {self._path}"
        )
    #============================================================#
    def reload(self):
        #------------------------------------------------------------#
        self._data = json_reader(
            self._path,
            {}
        )
        #------------------------------------------------------------#
        self._load_default()
        #------------------------------------------------------------#
        self.set_essential_values()
        #------------------------------------------------------------#
        self.set_dynamically_settings(
            self._data
        )
        #------------------------------------------------------------#
        log(
            f"{self.__class__.__name__} reloaded"
        )

