import pygame as pg
import pygame as np
#=====================================#
from engine.utils.log import log_error
#=====================================#
class TextRender:
    #=====================================#
    def __init__(self, main, render):
        #=====================================#
        self.main = main
        self.render = render
    
    #=====================================#
    def text(self, surface:pg.Surface, text:str, pos:tuple, font_name:str="AtariSmall", size:int=20, color:tuple=(255,255,255), aligment="topleft"):
        #--------------------------------#
        font = self.render.fonts.get(font_name)
        if not font:
            # font = AtariSmall
            log_error(f"Font '{font_name}' not found. Using default font 'AtariSmall'.")
        #--------------------------------#
        font.render(surface, pos, text, size=size, color=color, aligment=aligment)

    #=====================================#
    def draw_wrapped_text(self,
        surface:pg.Surface, text:str, pos:list, font_name:str="AtariSmall",
        size:int=16, color:tuple=(255,255,255), max_width:int=100, line_spacing:int=4):
        #--------------------------------#
        font = self.render.fonts.get(font_name)
        words = text.split()
        #--------------------------------#
        lines = []
        current_line = ""
        #--------------------------------#
        for word in words:
            #--------------------------------#
            test = word if not current_line else f"{current_line} {word}"
            #--------------------------------#
            if font.size(test)[0] <= max_width:
                current_line = test
            #--------------------------------#
            else:
                lines.append(current_line)
                current_line = word
        #--------------------------------#
        if current_line:
            lines.append(current_line)
        x, y = pos
        #--------------------------------#
        for line in lines:
            font.render(surface, pos, line, size=size, color=color, aligment="topleft")
            y += font.get_height() + line_spacing


