import pygame as pg
#================================#
from engine.utils.log import log,log_error,log_list,log_success
#--------------------------------#
from engine.configs.settings import settings
#--------------------------------#
from engine.console.ui import ConsoleUI
from engine.console.core import ConsoleCore
#================================#
size = settings.get("console_size", [320, 200])
input_size = settings.get("console_input_size", [300, 150])
output_size = settings.get("console_output_size", [300, 50])
#================================#
class Console:
    def __init__(self):
        #--------------------------------#
        self.core = ConsoleCore(self)
        self.ui = ConsoleUI(self, size, input_size, output_size)
        #--------------------------------#
        self.log = self.core.log
        self.log_error = self.core.error
        self.log_success = self.core.success
        self.log_command = self.core.command_log
        #--------------------------------#
        self.visible = False
    #--------------------------------#
    def draw(self, surface:pg.Surface):
        #--------------------------------#
        if self.visible:
            #--------------------------------#
            self.ui.draw(surface)
    #--------------------------------#
    def events(self, event):
        self.core.events(event)
#================================#
console = Console()
#================================#


