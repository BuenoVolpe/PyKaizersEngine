import pygame as pg
from sys import exit, executable, argv
import os
#--------------------------------#
from pathlib import Path
#--------------------------------#
from engine.utils.log import log, log_success, log_error
from engine.utils.json import json_reader, json_writer
#--------------------------------#
class Configs:
    #--------------------------------#
    def __init__(self, path:str="assets/config/settings.json"):
        #--------------------------------#
        self._path = Path(path)
        self._data = json_reader(path)
        #--------------------------------#
        # Dynamically set any additional settings from the JSON file
        for key, value in self._data.items():
            setattr(self, key, value)
        #--------------------------------#
        self.set_essential_values()
    #--------------------------------#
    def set_essential_values(self):
        """set default values for essential configs if they are not provided in the JSON"""
        ...
    #----get method---#
    def get(self, key:str, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        return default
    #----set method---#
    def set(self, key:str, value=None):
        #--------------------------------#
        if callable(getattr(self, key, None)):
            raise ValueError(f"Cannot overwrite method '{key}'")
        #--------------------------------#
        setattr(self, key, value)
        #--------------------------------#
        self._data[key] = value
        #--------------------------------#
        self.save()
    #----save method---#
    def save(self):
        #--------------------------------#
        json_writer(self._path, self._data)
        log_success(f"{self.__class__.__name__} saved: {self._path}")

    #----reload method---#
    def reload(self):
        #--------------------------------#
        self._data = json_reader(self._path)
        self.set_essential_values()
        #--------------------------------#
        for key, value in self._data.items():
            setattr(self, key, value)
        #--------------------------------#
        log(f"{self.__class__.__name__} reloaded")
#--------------------------------#

