import pygame as pg
from pathlib import Path
#=====================================#
from engine.configs import configs
#-------------------------------------#
from engine.handlers.texture.texture_data import TextureData
from engine.resource_string.resource_reference import ResourceReference
#-------------------------------------#
from engine.utils.json import json_reader
from engine.utils.log import printlog
from engine.utils.dict_to_class import dict_to_class
#-------------------------------------#
from game.globalclasses import globalclasses
#=====================================#
class Loader:
    #=====================================#
    def __init__(self, parent:object):
        #-------------------------------------#
        self.parent = parent
    #=====================================#
    def unload(self, resource):
        ...
    #=====================================#
    def load(self, resource:str) -> pg.Surface:
        #-------------------------------------#
        try:
            if resource not in self.parent._atlas:
                self.parent.register(resource)
            reference:ResourceReference = globalclasses.resource_string_manager.parse(resource)
            texture_data:TextureData = self.parent._atlas[reference.string]
            #-------------------------------------#
            metadata = json_reader(texture_data.json_path, {}) if texture_data.json_path else {}
            #-------------------------------------#
            if texture_data.image is None:
                #-------------------------------------#
                if metadata.get("convert_alpha"):
                    texture_data.image = pg.image.load(texture_data.path).convert_alpha()
                    texture_data.initial_image = texture_data.image.copy()
                #-------------------------------------#
                elif not metadata.get("convert_alpha"):
                    texture_data.image = pg.image.load(texture_data.path).convert()
                    texture_data.initial_image = texture_data.image.copy()
            #-------------------------------------#
            texture_data = self._apply_parametters(texture_data, metadata)
            #-------------------------------------#
            return texture_data.image
        #-------------------------------------#
        except FileExistsError as e:
            printlog.error(resource)
            printlog.error(e)
    #=====================================#
    def _apply_parametters(self, texture_data:TextureData, metadata:dict) -> TextureData:
        #-------------------------------------#
        resource_ref:ResourceReference = globalclasses.resource_string_manager.parse(
            texture_data.resource
        )
        #-------------------------------------#
        parametters = resource_ref.parameters
        #-------------------------------------#
        for key, value in parametters.items():
            metadata[key] = value
        #-------------------------------------#
        metadata = dict_to_class(metadata)
        #=====================================#
        width:int = metadata.get("width") or texture_data.image.get_width()
        height:int = metadata.get("height") or texture_data.image.get_height()
        angle:float = metadata.get("angle", 0)
        #=====================================#
        texture_data.parameters = parametters
        #-------------------------------------#
        texture_data.image = pg.transform.scale(texture_data.initial_image, [width, height])
        texture_data.image = pg.transform.rotate(texture_data.initial_image, angle)
        #-------------------------------------#
        return texture_data
