import pygame as pg
import time
#==============================================#
from engine.utils.sort_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#----------------------------------------------#
from engine.utils.log import printlog
# from engine.configs import configs
#----------------------------------------------#
from game.main.renderer.images import add_image, remove_image, draw_images
#==============================================#
# from engine.signal_bus import signal_bus
# from game.enums.signals import signals
# from game.enums.signals_priotity import signals_priority as sigprio
#==============================================#
class Renderer:
    #==============================================#
    def __init__(self):
        #----------------------------------------------#
        # self.ui_elements:list[dict] = [] #{"object":object, "name":name, "piority":num}
        # self.layers:list[dict] = [] #{"object":object, "name":name, "piority":num}
        self.images:list[dict] = [] #{"image":image, "name":name, "piority":num, "position": [x,y]}
        #----------------------------------------------#
        # self.add_image(pg.image.load("assets/engine/important/error/error.png"), name="error", position=[30,30])
        #----------------------------------------------#
        # signal_bus.subscribe(signals.UPDATER_ADD_OBJECT, self.add_image, priority=sigprio.ADD_OBJ)
        # signal_bus.subscribe(signals.UPDATER_REMOVE_OBJECT, self.remove_image, priority=sigprio.REMOVE_OBJ)
    #==============================================#
    def draw(self, main_surface:pg.Surface, display:pg.Surface, delta_time:float):
        #----------------------------------------------#
        display.fill([30,30,30])
        main_surface.fill([30,30,30])
        #----------------------------------------------#
        draw_images(self.images, main_surface)
        #----------------------------------------------#
        self.blit(main_surface, display)
    #----------------------------------------------#
    def blit(self, main_surface:pg.Surface, display:pg.Surface):
        resize_main_surface:bool = True
        if resize_main_surface:
        # if configs.game.resize_main_surface:
            surface = pg.transform.scale(main_surface, [320,180])
            display.blit(surface, [0,0])
        else:
            display.blit(main_surface, [0,0])
    #==============================================#
    def add_image(self, image:pg.Surface, name:str=None, priority:int=None, position:list=[0,0]):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            self.images:list = add_image(self.images, image, name, priority, position)
            printlog.success(f"image {name} was add to render's images")
        #----------------------------------------------#
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"image cannot add {name} to render's images; \n {e}")
    #----------------------------------------------#
    def remove_image(self, name:str):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            self.images:list = remove_image(self.images, name)
            printlog.success(f"image {name} was removed from render's images")
        #----------------------------------------------#
        except Exception as e:
            printlog.error(f"image cannot remove {name} from render's images; \n {e}")