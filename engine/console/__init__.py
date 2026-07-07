import pygame as pg
#=====================================#
from engine.configs.configs import configs
#=====================================#
from engine.console.utils import parse_args, parse_value, split_command
from engine.console.console_log import ConsoleLog
#=====================================#
from engine.utils.debug_log import log_error, log_success, log, log_dict, log_list
from engine.utils.scaler import scaler
#=====================================#
from engine.handlers.text_input import TextInput
from engine.handlers.fonts import fonts
#=====================================#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#=====================================#
class Console:
    def __init__(self):
        #-------------------------------------#
        self.visible = False
        self.cursor_timer = 0
        self.scroll_offset = 0 #px
        #-------------------------------------#
        self.commands = {}
        self.input = TextInput()
        self.console_log = ConsoleLog()
        self.font = fonts.get(configs.console.font).get_size(configs.console.font_size)
        #-------------------------------------#
        self._load_surface()
        #-------------------------------------#
        self.protection_level = configs.console.level
        signal_bus.subscribe(signals.EXECUTE_COMMAND, self.execute_command, priority=signals_prioritys.PRE_LAST)
        #-------------------------------------#
    #=====================================#
    def draw(self, screen:pg.Surface, dt:float):
        #-------------------------------------#
        if not self.visible:
            return
        #-------------------------------------#
        self.cursor_timer += dt
        #-------------------------------------#
        self.surface.fill(configs.console.output_color)
        self.draw_outline()
        #-------------------------------------#
        padding_y = scaler.constant(configs.console.padding_y) if configs.console.use_constant_scale else configs.console.padding_y
        padding_x = scaler.constant(configs.console.padding_x) if configs.console.use_constant_scale else configs.console.padding_x
        y = padding_y
        #-------------------------------------#
        base_x = padding_x
        base_y = self.RES.y - self.font.get_height() - padding_y

        prefix = "> "
        if self.input.has_selection():
            start, end = sorted([
                self.input.selection_start,
                self.input.selection_end
            ])

            left = prefix + self.input.text[:start]
            selected = self.input.text[start:end]

            x = base_x + self.font.size(left)[0]
            w = self.font.size(selected)[0]

            pg.draw.rect(
                self.surface,
                (60, 120, 255),
                (x, base_y, w, self.font.get_height())
            )

        #-------------------------------------#
        for line in self.console_log.lines[-configs.console.visible_lines:]:
            #-------------------------------------#
            img = self.font.render(
                line.text,
                True,
                self.parse_color(line.color)
            )
            #-------------------------------------#
            self.surface.blit(img, (padding_x, y))
            #-------------------------------------#
            y += self.font.get_height() + configs.console.line_spacing
        #-------------------------------------#
        self._draw_input(
            self.surface,
            padding_x,
            padding_y
        )
        #-------------------------------------#
        screen.blit(self.surface, self.pos)
    #=====================================#
    def handle_event(self, event):
        if not self.visible:
            return
        #-------------------------------------#
        result = self.input.handle_event(event)
        #-------------------------------------#
        if result is None:
            return
        #-------------------------------------#
        if result.startswith("__"):
            return
        #-------------------------------------#
        self.execute_command(result)
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
    def _draw_input(self, surface, padding_x, padding_y):
        #-------------------------------------#
        prefix = "> "
        #-------------------------------------#
        self._update_input_scroll(
            padding_x,
            prefix
        )
        #-------------------------------------#
        prefix_width = self.font.size(prefix)[0]
        cursor_width = scaler.constant(configs.console.cursor_width) if configs.console.use_constant_scale else configs.console.cursor_width
        #-------------------------------------#
        base_y = (
            self.RES.y
            - self.font.get_height()
            - padding_y
        )
        #-------------------------------------#
        text_surface = self.font.render(
            self.input.text,
            True,
            (255, 255, 255)
        )
        #-------------------------------------#
        clip = pg.Rect(
            padding_x + prefix_width,
            base_y,
            self.RES.x - padding_x * 2 - prefix_width,
            self.font.get_height()
        )
        #-------------------------------------#
        old_clip = surface.get_clip()
        surface.set_clip(clip)
        #-------------------------------------#
        surface.blit(
            text_surface,
            (
                padding_x + prefix_width - self.input.scroll_offset,
                base_y
            )
        )
        #-------------------------------------#
        surface.set_clip(old_clip)
        #-------------------------------------#
        prefix_surface = self.font.render(
            prefix,
            True,
            (255,255,255)
        )
        #-------------------------------------#
        surface.blit(
            prefix_surface,
            (padding_x, base_y)
        )
        #-------------------------------------#
        cursor_pixel = self.font.size(
            self.input.text[:self.input.cursor_pos]
        )[0]
        #-------------------------------------#
        cursor_x = (
            padding_x
            + prefix_width
            + cursor_pixel
            - self.input.scroll_offset
        )
        #-------------------------------------#
        if self.cursor_timer > 1:
            self.cursor_timer = 0
        #-------------------------------------#
        if self.cursor_timer < 0.5:
            before = "> " + self.input.text[:self.input.cursor_pos]
            #-------------------------------------#
            cursor_x = self.font.size(before)[0]
            #-------------------------------------#
            cursor_y = self.RES.y - self.font.get_height() - padding_y
            #if cursor is at the end of the text, draw a vertical line
            #-------------------------------------#
            if self.input.cursor_pos == len(self.input.text):
                #-------------------------------------#
                pg.draw.line(
                    self.surface,
                    (255,255,255),
                    (padding_x + cursor_x*1.05, cursor_y),
                    (padding_x + cursor_x*1.1,
                    cursor_y + self.font.get_height()),
                    cursor_width
                )
                #-------------------------------------#
            else:
                #-------------------------------------#
                pg.draw.line(
                    self.surface,
                    (255,255,255),
                    (padding_x + cursor_x, base_y),
                    (padding_x + cursor_x, base_y + self.font.get_height()),
                    cursor_width
                )
    #=====================================#
    def _update_input_scroll(self, padding_x: int, prefix: str):
        prefix_width = self.font.size(prefix)[0]

        available_width = (
            self.RES.x
            - (padding_x * 2)
            - prefix_width
        )

        cursor_text = self.input.text[:self.input.cursor_pos]
        cursor_pixel = self.font.size(cursor_text)[0]

        cursor_margin = self.font.size(" ")[0] * 2

        left_limit = self.input.scroll_offset
        right_limit = (
            self.input.scroll_offset
            + available_width
        )

        if cursor_pixel < left_limit + cursor_margin:
            self.input.scroll_offset = max(
                0,
                cursor_pixel - cursor_margin
            )

        elif cursor_pixel > right_limit - cursor_margin:
            self.input.scroll_offset = (
                cursor_pixel
                - available_width
                + cursor_margin
            )
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
    def log_dict(self, dict:dict,
                value_color:str=None,
                styles:list[str|None, str|None]=[],
                dict_name=None, name_color:str=None, name_styles:list[str|None, str|None]=None):
        self.console_log.log_dict(dict, value_color, styles, dict_name, name_color, name_styles)
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
            log_error(f"command '{cmd_name}' is unknown")
            self.log_error(f"command '{cmd_name}' is unknown")
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
            self.log_error(e)
            log_error(e)

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

