#=====================================#
import pygame as pg
from sys import exit
#=====================================#
class Display:
    #=====================================#
    def __init__(self):
        self._load_screen()
    #=====================================#
    def _load_screen(self):
        #-------------------------------------#
        res = [320,180]
        #-------------------------------------#
        self.screen = pg.display.set_mode(res)
        self.main_surface = pg.Surface(res)
        #-------------------------------------#
        pg.display.set_caption("PyKaizers Engine")
    #=====================================#
    
