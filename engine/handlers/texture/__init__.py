import pygame as pg
#-------------------------------------#
from engine.configs import configs
#-------------------------------------#
from engine.handlers.texture.atlas import TextureAtlas
from engine.handlers.texture.loader import TextureLoader
from engine.handlers.texture.registry import TextureRegistry
from engine.handlers.texture.texture_data import TextureData
from engine.handlers.texture.transformer import TextureTransformer
#-------------------------------------#
from engine.resource_string.resource_reference import ResourceReference
#-------------------------------------#
from engine.utils.json import json_reader
from engine.utils.log import printlog
#-------------------------------------#
from game.globalclasses import globalclasses
#=====================================#
class TextureHandler:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self._atlas:TextureAtlas = TextureAtlas()
        self._registry:TextureRegistry = TextureRegistry(self._atlas, globalclasses.resource_string_manager)
        self._loader:TextureLoader = TextureLoader()
        self._transformer:TextureTransformer = TextureTransformer()
        #-------------------------------------#
        self._create_error_texture()
    #=====================================#
    def get(self, resource_string:str) -> pg.Surface:
        #-------------------------------------#
        resource:ResourceReference = globalclasses.resource_string_manager.parse(resource_string)
        string:str = resource.string
        #-------------------------------------#
        texture_data:TextureData = self._atlas.get(string)
        if texture_data is None:
            printlog.error(f"cant find resource {resource_string}. Retuning error image")
            return self.error_texture
        #-------------------------------------#
        if texture_data.image is None:
            texture_data:TextureData = self.load(resource_string)
        #-------------------------------------#
        texture_data.image = self._transformer.transform(texture_data, resource.temporary_parameters)
        #-------------------------------------#
        return texture_data.image
    #=====================================#
    def get_texture_data(self, resource_string:str) -> TextureData | None:
        #-------------------------------------#
        string:ResourceReference = globalclasses.resource_string_manager.parse(resource_string).string
        #-------------------------------------#
        return self._atlas.get(string)
    #=====================================#
    def register(self, resource_string:str) -> TextureData:
        return self._registry.register(resource_string)
    #=====================================#
    def add(self, texture_data:TextureData):
        self._atlas.add(texture_data)
    #=====================================#
    def load(self, resource_string:TextureData) -> TextureData:
        #-------------------------------------#
        texture_data:TextureData = self.get_texture_data(resource_string)
        if texture_data is None:
            texture_data = self.register(resource_string)
        #-------------------------------------#
        texture_data:TextureData = self._loader.load(texture_data)
        #-------------------------------------#
        parameters = texture_data.parameters
        if texture_data.path:
            #-------------------------------------#
            for key, value in json_reader(texture_data.json_path).items():
                parameters[key] = value
        #-------------------------------------#
        texture_data.image = self._transformer.transform(texture_data, texture_data.parameters)
        #-------------------------------------#
        return texture_data
    #=====================================#
    def _create_error_texture(self):
        #-------------------------------------#
        image = pg.image.load(
            configs.paths.error_image
        ).convert()
        #-------------------------------------#
        texture = TextureData(
            resource=(
                f"{configs.engine.resource_type_marks.texture}"
                f"{configs.engine.resource_strings_seps.type}"
                f"{configs.engine.acronym}"
                f"{configs.engine.resource_strings_seps.namespace}"
                "error"
                ),
            path=configs.paths.error_image,
            image=image,
            initial_image=image.copy(),
            parameters={}
        )
        #-------------------------------------#
        self._atlas.add(texture)
        #-------------------------------------#
        self.error_texture = texture
    #=====================================#


# dave_width_30 = self.texture_handler.load("texture@pyk::dave?width=30")
# self.renderer.add_image(dict_to_class({
#     "image": dave_width_30.image,
#     "name": "texture@pyk::dave?width=30",
#     "priority": 0,
#     "position": [0, 0],
# }))
# dave_width_30 = self.texture_handler.load("texture@pyk::folder.dave?width=30")
# self.renderer.add_image(dict_to_class({
#     "image": dave_width_30.image,
#     "name": "texture@pyk::folder.dave?width=30",
#     "priority": 0,
#     "position": [0, 70],
# }))
# dave_width_50 = self.texture_handler.get("texture@pyk::folder.dave?#width=100")
# self.renderer.add_image(dict_to_class({
#     "image": dave_width_50,
#     "name": "texture@pyk::folder.dave?#width=30",
#     "priority": 0,
#     "position": [100, 0],
# }))

