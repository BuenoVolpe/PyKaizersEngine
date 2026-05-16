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
        self.commands = {} #command: [func, protection]
        self.console_permition = settings.get("console_permition", 0)
        #--------------------------------#
        self.core = ConsoleCore(self)
        self.ui = ConsoleUI(self, size, input_size, output_size)
        #--------------------------------#
        self.log = self.core.console_log.log
        self.log_error = self.core.console_log.error
        self.log_success = self.core.console_log.success
        self.log_command = self.core.console_log.command_log
        #--------------------------------#
        self.visible = False
    #--------------------------------#
    def register(self, name, func, protection_level:int=1):
        #--------------------------------#
        parts = name.split(".")
        node = self.commands
        #--------------------------------#
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            node = node[part]
        #--------------------------------#
        node[parts[-1]] = {
            "func": func,
            "help": func.__doc__ or "No description",
            "protection":protection_level
        }

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
def command(name, protection_level:int=1, groups=[]):
    """protection level 0 -> 3
        0:not cheats
        1:simple cheats
        2:more heavy cheats, can cause some problens 
        3:commands that could broke the game
    """
    #--------------------------------#
    def wrapper(func):
        #--------------------------------#
        for group in groups:
            #--------------------------------#
            if group == "None":
                #--------------------------------#
                console.register(f"{name}", func, protection_level)
                continue
            #--------------------------------#
            console.register(f"{group}.{name}", func, protection_level)
        #--------------------------------#
        console.register(name, func, protection_level)
        return func
    #--------------------------------#
    return wrapper


