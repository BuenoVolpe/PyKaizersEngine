import pygame as pg
from sys import exit
import time
#================================#
class Display:
    #================================#
    def __init__(self, main:object):
        self._load_screen()
    #================================#
    def _load_screen(self):
        self.main_surface = pg.Surface([320,180])
        #--------------------------------#
        self.screen = pg.display.set_mode([640,360])
        pg.display.set_caption("pykaizersEngine")
        #--------------------------------#
        pg.scrap.init()


