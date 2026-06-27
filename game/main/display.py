#=====================================#
import pygame as pg
from sys import exit
#=====================================#
from engine.configs.configs import configs
#=====================================#
class Display:
    #=====================================#
    def __init__(self):
        self._load_screen()
    #=====================================#
    def _load_screen(self):
        RES:list[int, int] = configs.game.window_size
        MIN_RES:list[int, int] = configs.game.base_window_size
        window_title:str = configs.game.window_title
        #--------------------------------#
        self.screen = pg.display.set_mode(RES)
        self.main_surface = pg.Surface(MIN_RES)
        #--------------------------------#
        pg.display.set_caption(window_title)
        #--------------------------------#
        pg.scrap.init()
    #=====================================#
    
