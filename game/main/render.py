import pygame as pg
import numpy as np
#=====================================#
from engine.utils.log import log_error
from game.main.text_render import TextRender
#================================#
from game.main.loader import loader
#================================#
class Render:
    #=====================================#
    def __init__(self, main):
        #--------------------------------#
        self.main = main
        self.text = TextRender(self.main, self)
        #--------------------------------#
        self.ui_elements:dict = {} #[priority, [elements]]
        self.layers:dict = {} #name: [priority, [elements]]
        #--------------------------------#
        self.systems:list = loader._load_render_systems()
        self.fonts:dict = loader._load_fonts()
    #=====================================#
    def render(self, surface:pg.Surface):
        ...
    def render_on_screen(self, screen:pg.display):
        ...
    def draw(self, main_surface:pg.Surface, screen:pg.display, dt:float):
        #--------------------------------#
        screen.fill((30,30,30))
        main_surface.fill((30,30,30))
        scaled_main_surface = main_surface
        #--------------------------------#
        # if settings.resize:
        scaled_main_surface = pg.transform.scale(main_surface, [640,360])
        #--------------------------------#
        screen.blit(scaled_main_surface, (0, 0))
    #=====================================#
    def add_layer(self, name:str, priority:int=0):
        #--------------------------------#
        self.layers.setdefault(name, []).append((priority, []))
        #--------------------------------#
        self.layers[name].sort(key=lambda x: x[0])

    #=====================================#
    def add_ui(self, elements:list, priotiry:int):
        self.ui_elements.append([priotiry, elements])
        self.ui_elements.sort(key=lambda x: x[0])

    #=====================================#
    def add_to_layer(self, layer_name:str, elements:list):
        for element in elements:
            self.layers[layer_name][0].append(element)



#=====================================#
def buffer_to_surface(buffer):
    r = ((buffer >> 16) & 0xFF).astype(np.uint8)
    g = ((buffer >> 8) & 0xFF).astype(np.uint8)
    b = (buffer & 0xFF).astype(np.uint8)

    rgb = np.dstack((r,g,b))
    rgb = np.transpose(rgb, (1,0,2))

    return pg.surfarray.make_surface(rgb)



