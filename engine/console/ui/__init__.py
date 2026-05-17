import pygame as pg
#================================#
from engine.configs.settings import settings
from engine.utils.recolor import darken_color
from engine.utils.scaler import scaler
#--------------------------------#
from engine.console.ui.surface import ConsoleSurface
from engine.console.ui.lines import ConsoleLines
#--------------------------------#
from game.fonts import fonts, AtariSmall
#================================#
size = settings.get("console_size", [320, 200])
input_size = settings.get("console_input_size", [300, 150])
output_size = settings.get("console_output_size", [300, 50])
#--------------------------------#
class ConsoleUI:
    def __init__(self, parent, size=size, input_size=input_size, output_size=output_size):
        self.parent = parent
        #--------------------------------#
        font_name = settings.get("console_font")
        font_size = settings.get("console_font_size")
        font = fonts.get(font_name, AtariSmall)
        self.console_font = font.get_size(font_size)
        #--------------------------------#
        self.console_surface = ConsoleSurface(size, input_size, output_size)
        self.console_lines = ConsoleLines(self, parent)
        #--------------------------------#
        self.surface = self.console_surface.surface
        self.surface_rect = self.console_surface.rect
    #================================#
    def reload(self):
        #--------------------------------#
        self.console_surface = ConsoleSurface(
            size=settings.get("console_size", [320, 200]),
            input_size=settings.get("console_input_size", [300, 150]),
            output_size=settings.get("console_output_size", [300, 50])
        )
        #--------------------------------#
        font_name = settings.get("console_font")
        font_size = settings.get("console_font_size")
        font = fonts.get(font_name, AtariSmall)
        self.console_font = font.get_size(font_size)
        #--------------------------------#
        self.console_lines = ConsoleLines(self, self.parent)
        #--------------------------------#
        self.surface = self.console_surface.surface
        self.surface_rect = self.console_surface.rect
    #================================#
    def draw(self, surface:pg.Surface):
        #--------------------------------#
        self.console_surface.clean_surface()
        self.console_lines.draw(self.surface, screen=surface)
        #--------------------------------#
        surface.blit(self.surface, self.surface_rect)
    #================================#



