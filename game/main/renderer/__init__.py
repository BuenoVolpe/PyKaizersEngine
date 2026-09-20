import pygame as pg
import time
#==============================================#
from engine.utils.order_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#==============================================#
from game.main.renderer.images import add_image, remove_image, draw_images
#==============================================#
class Renderer:
    #==============================================#
    def __init__(self):
        #----------------------------------------------#
        # self.ui_elements:list[dict] = [] #{"object":object, "name":name, "piority":num}
        # self.layers:list[dict] = [] #{"object":object, "name":name, "piority":num}
        self.images:list[dict] = [] #{"image":image, "name":name, "piority":num, "position": [x,y]}
        #----------------------------------------------#
        self.add_image(pg.image.load("assets/engine/important/error/error.png"), name="error", position=[30,30])
    #==============================================#
    def draw(self, display:pg.Surface):
        #----------------------------------------------#
        display.fill([30,30,30])
        #----------------------------------------------#
        draw_images(self.images, display)
    #==============================================#
    def add_image(self, image:pg.Surface, name:str=None, priority:int=None, position:list=[0,0]):
        self.images:list = add_image(self.images, image, name, priority, position)
    def remove_image(self, name:str):
        self.images:list = remove_image(self.images, name)
