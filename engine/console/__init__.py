import pygame as pg
#=====================================#
from engine.configs.configs import configs
#=====================================#
from engine.console.utils import parse_args, parse_value, split_command
from engine.console.console_log import ConsoleLog
#=====================================#
from engine.utils.debug_log import log_error, log_success, log, log_dict, log_list
from engine.utils.scaler import scaler
from engine.handlers.fonts import fonts
#=====================================#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#=====================================#
class Console:
    def __init__(self):
        #-------------------------------------#
        self.visible = True
        #-------------------------------------#
        self.commands = {}
        self.console_log = ConsoleLog()
        self.font = fonts.get(configs.console.font).get_size(configs.console.font_size)
        #-------------------------------------#
        self._load_surface()
        #-------------------------------------#
        self.protection_level = configs.console.level
        signal_bus.subscribe(signals.EXECUTE_COMMAND, self.execute_command, priority=signals_prioritys.PRE_LAST)
        #-------------------------------------#
    #=====================================#
    def draw(self, screen:pg.Surface):
        #-------------------------------------#
        if not self.visible:
            return
        #-------------------------------------#
        self.surface.fill(configs.console.output_color)
        self.draw_outline()
        #-------------------------------------#
        y = configs.console.padding_y
        #-------------------------------------#
        for line in self.console_log.lines[-configs.console.visible_lines:]:
            #-------------------------------------#
            img = self.font.render(
                line.text,
                True,
                self.parse_color(line.color)
            )
            #-------------------------------------#
            self.surface.blit(img, (configs.console.padding_x, y))
            #-------------------------------------#
            y += self.font.get_height() + configs.console.line_spacing
        #-------------------------------------#
        screen.blit(self.surface, self.pos)
    #=====================================#
    def _load_surface(self):
        #-------------------------------------#
        if configs.console.use_constant_scale:
            RES = scaler.constant(configs.console.RES[0]), scaler.constant(configs.console.RES[1])
        else:
            RES = configs.console.RES
        #-------------------------------------#
        self.RES = pg.Vector2(RES)
        #-------------------------------------#
        self.surface = pg.Surface(self.RES)
        self.surface.fill(configs.console.output_color)
        #-------------------------------------#
        if width := configs.console.outline_width:
            width = scaler.constant(configs.console.outline_width) if configs.console.use_constant_scale else configs.console.use_constant_scale
            self.draw_outline = lambda: pg.draw.rect(self.surface, configs.console.outline_color, [0, 0, *self.RES], width=width) if configs.console.outline_width else None
        #-------------------------------------#
        H_W = self.RES.x//2
        H_H = self.RES.y//2
        self.pos = configs.settings.window_size[0]//2-H_W, configs.settings.window_size[1]//2-H_H

    #=====================================#
    def log(self, text, color="white", styles=None):
        self.console_log.log(str(text), color, styles)
    #=====================================#
    def log_error(self, text):
        self.console_log.log_error(text)
    #=====================================#
    def log_success(self, text):
        self.console_log.log_success(text)
    #=====================================#
    def log_command(self, text):
        self.console_log.log_command(text)
    #=====================================#
    def log_list(self, list:list, color:str="white", styles:list=None, list_name:str=None, list_color:str=None, list_styles:list=None):
        self.console_log.log_list(list, color, styles, list_name, list_color, list_styles)
    #=====================================#
    def parse_color(self, color:str):
        colors = {
            "BLACK": (75,75,75),
            "RED": (255,0,0),
            "GREEN": (0,255,0),
            "BLUE": (0,0,255),
            "YELLOW": (255,255,0),
            "MAGENTA": (255,0,255),
            "CYAN": (0,255,255),
            "WHITE": (255,255,255)
        }
        color = colors.get(color.upper(), "WHITE")
        return color
    #=====================================#
    def execute_command(self, string:str):
        #-------------------------------------#
        cmd_name, args_text = split_command(string)
        #-------------------------------------#
        self.log_command(f"{string}")
        #-------------------------------------#
        if cmd_name not in self.commands:
            log_error(f"command '{cmd_name}' is unknown", self)
            return
        #-------------------------------------#
        cmd = self.commands[cmd_name]
        #-------------------------------------#
        args, kwargs = parse_args(args_text)
        #-------------------------------------#
        try:
            result = cmd["func"](*args, **kwargs)
            #-------------------------------------#
            if result is not None:
                log_success(result, self)
        except Exception as e:
            log_error(e, self)
        self.visible = False

    #=====================================#
    def register(self, name:str, func, protection_level:int=1):
        #--------------------------------#
        node = self.commands
        key = name.replace(".", " ")
        #--------------------------------#
        node[key] = {
            "func": func,
            "help": func.__doc__ or "No description",
            "protection":protection_level
        }
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

