import pygame as pg
from pathlib import Path
#=====================================#
from engine.configs import configs
#-------------------------------------#
from engine.handlers.texture.texture_data import TextureData
from engine.handlers.texture.loader import Loader
#-------------------------------------#
from engine.resource_string.resource_reference import ResourceReference
#-------------------------------------#
from engine.utils.json import json_reader
from engine.utils.log import printlog
#-------------------------------------#
from game.globalclasses import globalclasses
#=====================================#
pg.init()
#=====================================#
class TextureHandler:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self._atlas:dict = {}
        self._loader:Loader = Loader(self)
        #-------------------------------------#
        self._error_texture:TextureData = TextureData(
            resource="",
            path=configs.paths.error_image,
            json_path=None,
            image=pg.image.load(configs.paths.error_image).convert(),
            initial_image=pg.image.load(configs.paths.error_image).convert(),
            parameters={}
            )
        self._atlas["texture@pyk::error"] = self._error_texture
    #=====================================#
    def load(self, resource:str) -> pg.Surface:
        return self._loader.load(resource)
    #=====================================#
    def get(self, resource:str)  -> pg.Surface:
        #-------------------------------------#
        reference:ResourceReference = globalclasses.resource_string_manager.parse(resource)
        string:str = reference.string
        #-------------------------------------#
        if string not in self._atlas:
            printlog.error(f"texture: {string} is not registred or does not exist, \n returning error image")
            return self._error_texture.image
        #-------------------------------------#
        texture:TextureData = self._atlas[string]
        if texture.image is None:
            self.load(resource)
        #-------------------------------------#
        image = self._apply_parameters(texture, resource)
        #-------------------------------------#
        return texture.image
    #=====================================#
    def _apply_parameters(self, texture_data:TextureData, resource:str) -> pg.image:
        #-------------------------------------#
        reference:ResourceReference = globalclasses.resource_string_manager.parse(resource)
        metadata = reference.temporary_parameters
        #=====================================#
        width:int = metadata.get("width") or texture_data.image.get_width()
        height:int = metadata.get("height") or texture_data.image.get_height()
        angle:float = metadata.get("angle", 0)
        #-------------------------------------#
        image = pg.transform.scale(texture_data.image, [width, height])
        image = pg.transform.rotate(texture_data.image, angle)
        return image

    #=====================================#
    def register(self, resource:str) -> TextureData:
        #-------------------------------------#
        reference:ResourceReference = globalclasses.resource_string_manager.parse(resource)
        path:str = reference.path.replace(".", "/") + f".{configs.engine.extensions.texture}"
        #-------------------------------------#
        if reference.namespace == configs.engine.acronym:
            path:Path = Path(configs.paths.engine.texture + path)
        #-------------------------------------#
        elif reference.namespace == configs.game.acronym:
            path:Path = Path(configs.paths.game.texture + path)
        #-------------------------------------#
        json_path:Path = path.with_suffix(".json")
        if not json_path.exists():
            json_path:str = None
        #-------------------------------------#
        texture_data:TextureData = TextureData(
            resource,
            path=path,
            json_path=json_path,
            image=None,
            initial_image=None,
            parameters=reference.parameters,
        )
        #-------------------------------------#
        self._atlas[reference.string] = texture_data
        #-------------------------------------#
        return texture_data

#=====================================#


