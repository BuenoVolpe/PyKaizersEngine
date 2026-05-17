import pygame as pg
#================================#
from engine.configs.settings import settings
from engine.utils.recolor import darken_color
from engine.utils.scaler import scaler
#================================#
size = settings.get("console_size", [320, 200])
input_size = settings.get("console_input_size", [300, 150])
output_size = settings.get("console_output_size", [300, 50])
default_outline_width = settings.get("outline_width", 2)
#--------------------------------#
class ConsoleSurface:
    def __init__(self, size=size, input_size=input_size, output_size=output_size):
        #--------------------------------#
        self.build_surface(size, input_size, output_size)

    #================================#
    def build_input_surface(self, input_size):
        self.input_size = input_size
        #--------------------------------#
        default_input_color = settings.get("console_default_input_color", (30,30,30))
        self.default_input_color = getattr(self, "console_default_input_color", default_input_color)
        #--------------------------------#
        self.input_surface = pg.Surface(self.input_size)
        self.clean_input_surface()
    #--------------------------------#
    def clean_input_surface(self):
        self.input_surface.fill(self.default_input_color)
        #--------------------------------#
        input_color_dark = darken_color((self.default_input_color))
        input_color_light = darken_color((self.default_input_color), 1.3)
        #--------------------------------#
        start_pos1 = [self.scaled_outline_width//2,self.scaled_outline_width//2]
        start_pos2 = [self.input_size[0]-self.scaled_outline_width//2,self.scaled_outline_width//2]
        start_pos3 = [self.scaled_outline_width//2,self.input_size[1]-self.scaled_outline_width]
        #--------------------------------#
        end_pos1 = [self.input_size[0]+self.scaled_outline_width//2,self.scaled_outline_width//2]
        end_pos2 = [self.scaled_outline_width//2, self.input_size[1]-self.scaled_outline_width//2]
        end_pos3 = [self.input_size[0]-self.scaled_outline_width//2, self.input_size[1]-self.scaled_outline_width]
        #--------------------------------#
        pg.draw.line(self.input_surface, input_color_dark,
                    start_pos1, end_pos1,
                    scaler.constant(self.line_width))
        pg.draw.line(self.input_surface, input_color_dark,
                    start_pos1, end_pos2,
                    scaler.constant(self.line_width))
        #--------------------------------#    
        pg.draw.line(self.input_surface, input_color_light,
                    start_pos2, end_pos3,
                    scaler.constant(self.line_width))
        pg.draw.line(self.input_surface, input_color_light,
                    start_pos3, end_pos3,
                    scaler.constant(self.line_width))
        #--------------------------------#    
        pg.draw.line(self.input_surface, (0,0,0),
                    (0,0), (self.input_size[0], 0),
                    scaler.constant(self.scaled_outline_width//2))
    #================================#
    def build_output_surface(self, output_size):
        self.output_size = output_size
        #--------------------------------#
        default_color = settings.get("console_default_color", (30,30,30))
        self.default_color = getattr(self, "default_color", default_color)
        #--------------------------------#
        self.output_surface = pg.Surface(self.output_size)
        self.clean_outpot_surface()
    def clean_outpot_surface(self):
        self.output_surface.fill(self.default_color)
        #--------------------------------#
        output_color_dark = darken_color((self.default_color))
        output_color_light = darken_color((self.default_color), 1.3)
        #--------------------------------#
        #--------------------------------#
        start_pos1 = [self.scaled_outline_width//2,self.scaled_outline_width//2]
        start_pos2 = [self.output_size[0]-self.scaled_outline_width//2,self.scaled_outline_width//2]
        start_pos3 = [self.scaled_outline_width//2,self.output_size[1]-self.scaled_outline_width]
        #--------------------------------#
        end_pos1 = [self.output_size[0]+self.scaled_outline_width//2,self.scaled_outline_width//2]
        end_pos2 = [self.scaled_outline_width//2, self.output_size[1]-self.scaled_outline_width//2]
        end_pos3 = [self.output_size[0]-self.scaled_outline_width//2, self.output_size[1]-self.scaled_outline_width]
        #--------------------------------#
        pg.draw.line(self.output_surface, output_color_dark,
                     start_pos1, end_pos1, scaler.constant(self.line_width))
        pg.draw.line(self.output_surface, output_color_dark,
                     start_pos1, end_pos2, scaler.constant(self.line_width))
        #--------------------------------#
        pg.draw.line(self.output_surface, output_color_light,
                     start_pos2, end_pos3, scaler.constant(self.line_width))
        pg.draw.line(self.output_surface, output_color_light,
                     start_pos3, end_pos3, scaler.constant(self.line_width))
    #================================#
    def save_console_personalization(self):
        #--------------------------------#
        console_personalization = {
            "console_line_width": 4,
            "console_outline_width": 1,
            "console_size": [200, 100],
            "console_input_size": [200, 25],
            "console_output_size": [200, 75],
            "console_default_color": [30, 30, 30],
            "console_selection_color": [80, 80, 160],
            "console_default_input_color": [100, 100, 100],
            
            "console_actived": True,
            "console_permition": 3,
            "console_actived_by_hotkey": True,
            
            "console_max_lines": 100,
            "console_max_visible_lines": 8,
            "console_max_autocomplete_candidates": 4,
            "console_output_padding": [2,1],
            "console_output_font": "atarismall",
            "console_output_font_size": 8
        }
        #--------------------------------#
        for key, value in console_personalization.items():
            settings.set(key, value)
    #================================#
    def build_surface(self, size, input_size, output_size, outline_width=default_outline_width):
        self.scaled_outline_width = scaler.constant(outline_width)
        #--------------------------------#
        size = scaler.constant(size[0]+outline_width), scaler.constant(size[1]+outline_width)
        input_size = scaler.constant(input_size[0]), scaler.constant(input_size[1])
        output_size = scaler.constant(output_size[0]), scaler.constant(output_size[1])
        #--------------------------------#
        self.size = size
        #--------------------------------#
        self.surface = pg.Surface(self.size)
        #--------------------------------#
        self.line_width = settings.get("console_line_width", 5)
        #--------------------------------#
        self.build_input_surface(input_size)
        self.build_output_surface(output_size)
        #--------------------------------#
        pg.draw.rect(self.surface, (0,0,0), (0,0,*self.size), self.scaled_outline_width)
        self.clean_surface()
        self.rect = self.surface.get_rect(center=settings.window_center)
    #================================#
    def clean_surface(self):
        output_pos = self.scaled_outline_width//2,self.scaled_outline_width//2
        input_pos = self.scaled_outline_width//2,self.output_size[1]+self.scaled_outline_width//2
        #--------------------------------#
        self.clean_input_surface()
        self.clean_outpot_surface()
        #--------------------------------#
        self.surface.blit(self.output_surface, output_pos)
        self.surface.blit(self.input_surface, input_pos)
    #================================#
