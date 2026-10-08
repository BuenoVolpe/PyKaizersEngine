import pygame as pg
import time
#==============================================#
from engine.utils.sort_list import sort_objects
from engine.utils.dict_to_class import dict_to_class
#----------------------------------------------#
from engine.utils.log import printlog
from engine.configs import configs
#----------------------------------------------#
from game.main.renderer.images import add_image, remove_image, draw_images
#============================================================#
from engine.signalbus import signalbus
from game.enums.signals import signals
from game.enums.signals_order import signals_order as sigorder
#============================================================#
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
        signalbus.subscribe(signals.RENDER_ADD_IMG, self.add_image, order=sigorder.ADDOBJ.FIRST)
        signalbus.subscribe(signals.RENDER_REMOVE_IMG, self.remove_image, order=sigorder.REMOVEOBJ.FIRST)
    #==============================================#
    def draw(self, main_surface:pg.Surface, display:pg.Surface, delta_time:float):
        #----------------------------------------------#
        main_surface.fill(configs.game.main_surface_background_color)
        display.fill(configs.game.background_color)
        #----------------------------------------------#
        draw_images(self.images, main_surface)
        #----------------------------------------------#
        self.blit(main_surface, display)
    #----------------------------------------------#
    def blit(self, main_surface:pg.Surface, display:pg.Surface):
        if configs.game.resize_main_surface:
            surface = pg.transform.scale(main_surface, [320,180])
            display.blit(surface, [0,0])
        else:
            display.blit(main_surface, [0,0])
    #==============================================#
    def add_image(self, ctxt:object):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            self.images:list = add_image(self.images, ctxt.image, ctxt.name, ctxt.priority, ctxt.position)
            printlog.success(f"image {ctxt.name} was add to render's images")
        #----------------------------------------------#
        except Exception as e:
            #----------------------------------------------#
            printlog.error(f"image cannot add {ctxt.name} to render's images; \n {e}")
    #----------------------------------------------#
    def remove_image(self, ctxt:object):
        #----------------------------------------------#
        try:
            #----------------------------------------------#
            self.images:list = remove_image(self.images, ctxt.name)
            # printlog.success(f"image {ctxt.name} was removed from render's images")
        #----------------------------------------------#
        except Exception as e:
            printlog.error(f"image cannot remove {ctxt.name} from render's images; \n {e}")