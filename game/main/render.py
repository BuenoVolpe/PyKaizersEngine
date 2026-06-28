#=====================================#
import pygame as pg
from sys import exit
#=====================================#
from engine.utils.log import log_error
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#=====================================#
class Render:
    #=====================================#
    def __init__(self):
        #=====================================#
        self.ui_elements = {} #priority: [elements]
        self.layers = {} #priority: [elements]
        #-------------------------------------#
        self.images = []
        #-------------------------------------#
        self.systems = [
            # RenderSystem(world)
        ]
        #=====================================#
        self._subscribe_functions()
    #=====================================#
    def _subscribe_functions(self):
        #-------------------------------------#
        signal_bus.subscribe(signals.RENDER_ADD_UI_ELEMENT, self.add_ui_element, sig_prio.ADD_OBJ)
        signal_bus.subscribe(signals.RENDER_REMOVE_UI_ELEMENT, self.remove_ui_element, sig_prio.REMOVE_OBJ)
        signal_bus.subscribe(signals.RENDER_ADD_OBJ, self.add_object, sig_prio.ADD_OBJ)
        signal_bus.subscribe(signals.RENDER_REMOVE_OBJ, self.remove_object, sig_prio.REMOVE_OBJ)
    #=====================================#
    def add_ui_element(self, element, priority:int=0):
        #-------------------------------------#
        if priority not in self.ui_elements:
            self.ui_elements[priority] = []
        #-------------------------------------#
        self.ui_elements[priority].append(element)
    #-------------------------------------#
    def remove_ui_element(self, element):
        for priority in self.ui_elements:
            if element in self.ui_elements[priority]:
                self.ui_elements[priority].remove(element)
                return
    #-------------------------------------#
    def add_object(self, element, priority:int=0):
        #-------------------------------------#
        if priority not in self.layers:
            self.layers[priority] = []
        #-------------------------------------#
        self.layers[priority].append(element)
    #-------------------------------------#
    def remove_object(self, element):
        for priority in self.layers:
            if element in self.layers[priority]:
                self.layers[priority].remove(element)
                return
    #=====================================#
    def render(self, surface:pg.Surface):
        #-------------------------------------#
        for image in self.images:
            surface.blit(image["texture"], image["pos"])
        #-------------------------------------#
        for priority in sorted(self.layers.keys()):
            for obj in self.layers[priority]:
                #-------------------------------------#
                if hasattr(obj, "render"):
                    obj.render(surface)
                    continue
                if hasattr(obj, "draw"):
                    obj.draw(surface)
                    continue
                #-------------------------------------#
                log_error(f"Object {obj} has no 'render' or 'draw' method.")
        #-------------------------------------#
        for system in self.systems:
            if not getattr(system, "on_screen", True):
                system.update(surface)
    #=====================================#
    def render_on_screen(self, screen:pg.Surface):
        for priority in sorted(self.ui_elements.keys()):
            for obj in self.ui_elements[priority]:
                #-------------------------------------#
                if hasattr(obj, "render"):
                    obj.render(screen)
                    continue
                if hasattr(obj, "draw"):
                    obj.draw(screen)
                    continue
                #-------------------------------------#
                log_error(f"UI Element {obj} has no 'render' or 'draw' method.")
        #-------------------------------------#
        for system in self.systems:
            if getattr(system, "on_screen", False):
                system.update(screen)
        #-------------------------------------#
    #=====================================#
    def draw(self, screen, surface, dt):
        #-------------------------------------#
        screen.fill((30,30,30))
        surface.fill((30,30,30))
        #-------------------------------------#
        self.render(surface)
        #-------------------------------------#
        scaled_surface = surface
        scaled_surface = pg.transform.scale(surface, screen.get_size())
        #-------------------------------------#
        screen.blit(scaled_surface, (0, 0))
        #-------------------------------------#
        self.render_on_screen(screen)
    #=====================================#
