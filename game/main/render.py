from engine.handlers.textures import TextureHandler
from engine.configs.settings import settings
#--------------------------------#
from engine.utils.log import log_error
from engine.utils.event_bus import event_bus
from game.fonts import *
#--------------------------------#
from engine.ecs.systems.all import RenderSystem
#--------------------------------#
from game.enums.events import events
from game.enums.layers import layers, ui_layers
#--------------------------------#
import pygame as pg
#=====================================#
class Render:
    #--------------------------------#
    def __init__(self, world):
        #--------------------------------#
        self.TextureHandler = TextureHandler()
        #--------------------------------#
        self.fonts = {
            "AtariSmall": AtariSmall,
            "dogicapixel": dogicapixel,
            "PixelOperator": PixelOperator,
        }
        #--------------------------------#
        self.ui_elements = {} #priority: [elements]
        self.layers = {} #priority: [elements]
        #--------------------------------#
        self.systems = [
            RenderSystem(world)
        ]
        #--------------------------------#
        event_bus.subscribe(events.ADD_UI_ELEMENT_TO_LAYER, self.add_ui_element, priority=3)
        event_bus.subscribe(events.REMOVE_UI_ELEMENT_FROM_LAYER, self.remove_ui_element, priority=3)
        event_bus.subscribe(events.ADD_OBJECT_TO_LAYER, self.add_object, priority=3)
        event_bus.subscribe(events.REMOVE_OBJECT_FROM_LAYER, self.remove_object, priority=3)
    #=====================================#
    def add_ui_element(self, element, priority:int=0):
        #--------------------------------#
        if priority not in self.ui_elements:
            self.ui_elements[priority] = []
        #--------------------------------#
        self.ui_elements[priority].append(element)
    #--------------------------------#
    def remove_ui_element(self, element):
        for priority in self.ui_elements:
            if element in self.ui_elements[priority]:
                self.ui_elements[priority].remove(element)
                return
    #--------------------------------#
    def add_object(self, element, priority:int=0):
        #--------------------------------#
        if priority not in self.layers:
            self.layers[priority] = []
        #--------------------------------#
        self.layers[priority].append(element)
    #--------------------------------#
    def remove_object(self, element):
        for priority in self.layers:
            if element in self.layers[priority]:
                self.layers[priority].remove(element)
                return
    #=====================================#
    def render(self, surface:pg.Surface):
        '''render objects on the main surface'''
        #--------------------------------#
        self.TextureHandler.blit("pyk::penguin::idle", surface, (50, 50))
        #--------------------------------#
        for priority in sorted(self.layers.keys()):
            for obj in self.layers[priority]:
                #--------------------------------#
                if hasattr(obj, "render"):
                    obj.render(surface)
                    continue
                if hasattr(obj, "draw"):
                    obj.draw(surface)
                    continue
                #--------------------------------#
                log_error(f"Object {obj} has no 'render' or 'draw' method.")
        #--------------------------------#
        for system in self.systems:
            if not getattr(system, "on_screen", True):
                system.update(surface)
            
    #--------------------------------#
    def render_on_screen(self, screen:pg.Surface):
        '''render objects straight on the screen surface, use only for UI elements that need to be on top of everything else'''
        #--------------------------------#
        self.text(screen, f"time: {pg.time.get_ticks()//1000}", (10, 10), font_name="AtariSmall", size=30)
        #--------------------------------#
        for priority in sorted(self.ui_elements.keys()):
            for obj in self.ui_elements[priority]:
                #--------------------------------#
                if hasattr(obj, "render"):
                    obj.render(screen)
                    continue
                if hasattr(obj, "draw"):
                    obj.draw(screen)
                    continue
                #--------------------------------#
                log_error(f"UI Element {obj} has no 'render' or 'draw' method.")
        #--------------------------------#
        for system in self.systems:
            if getattr(system, "on_screen", False):
                system.update(screen)
    #=====================================#
    def text(self, surface:pg.Surface, text:str, pos:tuple, font_name:str="AtariSmall", size:int=20, color:tuple=(255,255,255)):
        #--------------------------------#
        font = self.fonts.get(font_name)
        if not font:
            font = AtariSmall
            log_error(f"Font '{font_name}' not found. Using default font 'AtariSmall'.")
        #--------------------------------#
        font.render(surface, pos, text, size=size, color=color)
    #=====================================#
    def draw(self, screen:pg.Surface, main_surface:pg.Surface):
        #--------------------------------#
        screen.fill(settings.get("bg_color", (30,30,30)))
        main_surface.fill(settings.get("bg_color", (30,30,30)))
        #--------------------------------#
        self.render(main_surface)
        #--------------------------------#
        scaled_main_surface = main_surface
        if settings.resize:
            scaled_main_surface = pg.transform.scale(main_surface, settings.window_size)
        #--------------------------------#
        screen.blit(scaled_main_surface, (0, 0))
        #--------------------------------#
        self.render_on_screen(screen)

