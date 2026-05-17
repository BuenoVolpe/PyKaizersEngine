import pygame as pg
import inspect
import shlex
#--------------------------------#
from engine.console.core.log import ConsoleLog
from engine.console.core.executer import ConsoleExecute
from engine.console.core.suggestions import ConsoleSuggestions
#--------------------------------#
from engine.handlers.text_input import TextInput
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class ConsoleCore:
    def __init__(self, parent):
        #--------------------------------#
        self.show_signature = True
        #--------------------------------#
        self.parent = parent
        self.text_input = TextInput()
        self.console_log = ConsoleLog(self, parent)
        self.suggestions = ConsoleSuggestions(self, parent)
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
                #--------------------------------#
                if event.key not in [pg.K_RETURN, pg.K_TAB]:
                    self.suggestions.reset()
                #--------------------------------#
                if event.key == pg.K_PAGEUP:
                    self.scroll_y = max(0, self.scroll_y + 1)
                elif event.key == pg.K_PAGEDOWN:
                    self.scroll_y = min(self.scroll_y - 1, self.max_scroll())
            #--------------------------------#
            if result is not None:
                if result == "__TAB__":
                    #--------------------------------#
                    if self.suggestions.candidates:
                        #--------------------------------#
                        suggestion = self.suggestions.next()
                        #--------------------------------#
                        if suggestion:
                            text = self.text_input.text

                            parts = shlex.split(text)

                            if not parts:
                                parts = [""]

                            if text.endswith(" "):
                                parts.append("")

                            if len(parts) == 0:
                                parts = [""]

                            parts[-1] = suggestion
                            self.text_input.set_text(" ".join(parts))
                        #--------------------------------#
                        # self.suggestions.reset()
                    #--------------------------------#
                    return
                if result == "__BACKSPACE__":
                    self.suggestions.reset()
                    return
                #--------------------------------#
                self.suggestions.reset()
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


