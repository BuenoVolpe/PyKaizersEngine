import pygame as pg
#--------------------------------#
from engine.handlers.text_input import TextInput
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class ConsoleLog:
    def __init__(self, parent, grandparent):
        self.parent = parent
        self.grandparent = grandparent
    #--------------------------------#
    def log(self, text, color=(200, 200, 200), styles=[]):
        self._add_line(text, color)
    #--------------------------------#
    def error(self, text):
        self._add_line(f"!> {text}", (255, 80, 80))
    #--------------------------------#
    def success(self, text):
        self._add_line(f">> {text}", (255, 220, 90))
    #--------------------------------#
    def command_log(self, text):
        self._add_line(f"> {text}", (180, 180, 180))
    #================================#
    def _add_line(self, text, color):
        #--------------------------------#
        font = self.grandparent.ui.console_font
        #--------------------------------#
        max_width = (scaler.constant(settings.get("console_output_size", [300,0])[0]) 
                    -scaler.constant(settings.get("outline_width", 2))
                    -settings.get("console_line_width", 5))
        #--------------------------------#
        for chunk in text.split("\n"):
            #--------------------------------#
            wrapped_lines = self.grandparent.ui.console_lines.wrap_text(chunk, font, max_width)
            #--------------------------------#
            for line in wrapped_lines:
                self.parent.history.append((line, color))
        #--------------------------------#
        while len(self.parent.history) > self.parent.max_lines:
            #--------------------------------#
            self.parent.history.pop(0)

        