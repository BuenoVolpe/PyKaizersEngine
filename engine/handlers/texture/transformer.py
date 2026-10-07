import pygame as pg
#=====================================#
class TextureTransformer:
    #=====================================#
    def transform(self, texture_data, parameters:dict):
        #=====================================#
        if texture_data.initial_image is None:
            return None
        #-------------------------------------#
        image = texture_data.initial_image
        #-------------------------------------#
        width = parameters.get("width",image.get_width())
        height = parameters.get("height",image.get_height())
        angle = parameters.get("angle",0)
        #-------------------------------------#
        image = self._apply_size(image, width, height)
        image = self._apply_angle(image, angle)
        #-------------------------------------#
        return image
    #=====================================#
    def _apply_size(self, image:pg.Surface, width:int, height:int) -> pg.Surface:
        #-------------------------------------#
        if (width != image.get_width() or height != image.get_height()):
            image = pg.transform.scale(image,(width, height))
        #-------------------------------------#
        return image
    #=====================================#
    def _apply_angle(self, image:pg.Surface, angle:float) -> pg.Surface:
        #-------------------------------------#
        if angle != 0:
            #-------------------------------------#
            image = pg.transform.rotate(
                image,
                angle
            )
        #-------------------------------------#
        return image
    