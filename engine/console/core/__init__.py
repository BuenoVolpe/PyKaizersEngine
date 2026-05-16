import pygame as pg
#--------------------------------#
from engine.console.core.log import ConsoleLog
from engine.console.core.executer import ConsoleExecute
#--------------------------------#
from engine.handlers.text_input import TextInput
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class ConsoleCore:
    def __init__(self, parent):
        #--------------------------------#
        self.parent = parent
        self.log = parent
        self.text_input = TextInput()
        self.console_log = ConsoleLog(self, parent)
        self.executer = ConsoleExecute(self, parent)
        #--------------------------------#
        self.history = []
        self.max_lines = settings.get("console_max_lines", 100)
        self.scroll_y = 0
    #================================#
    def events(self, event):
        if self.parent.visible:
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
                self.console_log.command_log(text)
                success = self.executer.execute(text)
                #--------------------------------#
                # if success and text not in self.command_history:
                #     self.command_history.append(text)
                #     self.history_index = len(self.command_history)
    #================================#
    def max_scroll(self):
        return max(0, len(self.history) - self.parent.ui.visible_lines)
    #================================#
