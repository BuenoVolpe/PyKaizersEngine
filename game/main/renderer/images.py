import pygame as pg
import time
#==============================================#
from engine.utils.order_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#==============================================#
def add_image(images_list:list, image:pg.Surface, name:str=None, priority:int=None, position:list=[0,0]) -> list:
    #----------------------------------------------#
    if priority is None:
        priority:int = 999 
    #----------------------------------------------#
    if name is None:
        name:str = f"{image.__class__.__name__}.{time.time()}"
    #----------------------------------------------#
    image_ = dict_to_class({"image":image, "name":name, "piority":priority, "position":position})
    images_list.append(image_)
    #----------------------------------------------#
    return images_list
#==============================================#
def remove_image(images_list:list, name:str) -> list:
    #----------------------------------------------#
    for image in images_list.images.copy():
        #----------------------------------------------#
        if image.name == name:
            images_list.images.remove(image)
    #----------------------------------------------#
    return images_list
#==============================================#
def draw_images(images_list:list, display:pg.Surface):
    #----------------------------------------------#
    if images_list is None:
        return
    #----------------------------------------------#
    for image_info in images_list:
        #----------------------------------------------#
        display.blit(image_info.image, image_info.position)

