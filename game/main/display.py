import os
import pygame as pg
#--------------------------------#
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class Display:
    #--------------------------------#
    def __init__(self):
        self.load_screen()
    #================================#
    def load_screen(self):
        #--------------------------------#
        MIN_RES:tuple = settings.base_window_size
        RES:tuple = settings.window_size
        #--------------------------------#
        if settings.fullscreen:
            #------------------------------#
            os.environ["SDL_VIDEO_CENTERED"] = "1"
            info = pg.display.Info()
            #------------------------------#
            WIDTH:int = info.current_w
            HEIGHT:int = info.current_h
            RES:tuple = (WIDTH, HEIGHT)
            #------------------------------#            
            settings.window_width, settings.window_height = settings.window_size = RES
            settings.window_center = RES[0]//2, RES[1]//2
            #------------------------------#            
            scaler.update()
        #--------------------------------#
        MIN_RES:tuple = settings.base_window_size if settings.resize else RES
        #--------------------------------#
        self.main_surface = pg.Surface(MIN_RES)
        #--------------------------------#
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption(settings.window_title)
        #--------------------------------#
        pg.scrap.init()