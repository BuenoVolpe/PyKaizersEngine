import pygame as pg
#-------------------------------------#
from engine.utils.json import json_reader
from engine.utils.log import printlog
#-------------------------------------#
from engine.handlers.texture.texture_data import TextureData
#=====================================#
class TextureLoader:
    #=====================================#
    def load(self, texture_data:TextureData) -> TextureData:
        #-------------------------------------#
        try:
            #=====================================#
            metadata = {}
            if texture_data.json_path:
                metadata = json_reader(
                    texture_data.json_path,
                    {}
                )
            #=====================================#
            if texture_data.image is None:
                #-------------------------------------#
                if metadata.get("convert_alpha", False):
                    image = pg.image.load(
                        texture_data.path
                    ).convert_alpha()
                #-------------------------------------#
                else:
                    image = pg.image.load(
                        texture_data.path
                    ).convert()
                #-------------------------------------#
                texture_data.image = image
                texture_data.initial_image = image.copy()
            #=====================================#
            return texture_data
        #=====================================#
        except (FileNotFoundError, pg.error) as error:
            #-------------------------------------#
            printlog.error(
                f"Failed to load texture: {texture_data.resource}"
            )
            #-------------------------------------#
            printlog.error(error)
            #-------------------------------------#
            return None


        