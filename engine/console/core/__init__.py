import pygame as pg
#--------------------------------#
from engine.handlers.text_input import TextInput
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class ConsoleCore:
    def __init__(self, parent):
        #--------------------------------#
        self.parent = parent
        self.text_input = TextInput()
        #--------------------------------#
        self.history = []
        self.max_lines = settings.get("console_max_lines", 100)
        self.scroll_y = 0
    #================================#
    def events(self, event):
        #--------------------------------#
        result = self.text_input.handle_event(event)
        #--------------------------------#
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_PAGEUP:
                self.scroll_y = max(0, self.scroll_y + 1)
            elif event.key == pg.K_PAGEDOWN:
                self.scroll_y = min(self.scroll_y - 1, self.max_scroll())
        #--------------------------------#
        if result is not None:
            #--------------------------------#
            # self.autocomplete_candidates = []
            # self.autocomplete_index = 0
            #--------------------------------#
            text = result
            #--------------------------------#
            self.command_log(text)
            # success = self.execute(text)
            #--------------------------------#
            # if success and text not in self.command_history:
            #     self.command_history.append(text)
            #     self.history_index = len(self.command_history)
    #================================#
    def max_scroll(self):
        return max(0, len(self.history) - self.parent.ui.visible_lines)
    #================================#
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
        font = self.parent.ui.console_font
        #--------------------------------#
        max_width = (scaler.constant(settings.get("console_output_size", [300,0])[0]) 
                    -scaler.constant(settings.get("outline_width", 2))
                    -settings.get("console_line_width", 5))
        #--------------------------------#
        for chunk in text.split("\n"):
            #--------------------------------#
            wrapped_lines = self.parent.ui.console_lines.wrap_text(chunk, font, max_width)
            #--------------------------------#
            for line in wrapped_lines:
                self.history.append((line, color))
        #--------------------------------#
        while len(self.history) > self.max_lines:
            #--------------------------------#
            self.history.pop(0)

        