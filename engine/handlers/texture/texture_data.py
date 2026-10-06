import pygame as pg
#=====================================#
class TextureData:
    #-------------------------------------#
    def __init__(self, resource:str, path:str, json_path:str=None, image:pg.surface=None, initial_image:pg.surface=None, parameters:dict={}):
        #-------------------------------------#
        self.resource:str = resource
        self.path:str = path
        self.json_path:str = json_path
        #-------------------------------------#
        self.image:pg.surface = image
        self.initial_image:pg.surface = initial_image or image
        #-------------------------------------#
        self.parameters:dict = parameters
        #-------------------------------------#
        self._data:dict = {
            'resource': resource,
            'path': path,
            'json_path': json_path,
            'image': image,
            'initial_image': initial_image,
            'parameters': parameters,
        }
