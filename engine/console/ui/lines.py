import pygame as pg
#================================#
from engine.configs.settings import settings
from engine.utils.recolor import darken_color
from engine.utils.scaler import scaler
#--------------------------------#
from engine.console.ui.surface import ConsoleSurface
#--------------------------------#
from game.fonts import fonts, AtariSmall
#================================#
class ConsoleLines:
    def __init__(self, parent, grandparent):
        #--------------------------------#
        self.parent = parent
        self.grandparent = grandparent
        #--------------------------------#
        self.console_font = self.parent.console_font
        #--------------------------------#
        padding = settings.get("console_output_padding", [3,3])
        self.padding = scaler.constant(padding[0]), scaler.constant(padding[1])
    #================================#
    def draw_lines(self, surface):
        core = self.grandparent.core
        #--------------------------------#
        total_lines = len(core.history)
        #--------------------------------#
        visible_lines = settings.get("console_max_visible_lines", 9)
        scroll_y = max(0, min(core.scroll_y, max(0, total_lines - visible_lines)))
        #--------------------------------#
        start = max(0, total_lines - visible_lines - scroll_y)
        end = start + visible_lines
        #--------------------------------#
        lines_to_draw = core.history[start:end]
        y = self.parent.console_surface.scaled_outline_width + self.parent.console_surface.line_width//2
        #--------------------------------#
        for text, color in lines_to_draw:
            #--------------------------------#
            text_surface = self.console_font.render(text, False, color)
            surface.blit(text_surface, (self.padding[0], y))
            #--------------------------------#
            y += self.padding[1] + self.console_font.get_height()
    #================================#
    def get_visible_input(self, font, max_width):
        core = self.grandparent.core
        #--------------------------------#
        prefix = ">"
        text = core.text_input.text
        #--------------------------------#
        full = prefix + text
        #--------------------------------#
        cursor_px = font.render(prefix + text[:core.text_input.cursor_pos], False, (255,255,255)).get_width()
        #--------------------------------#
        visible = font.render(full, False, (255,255,255))
        #--------------------------------#
        return visible, cursor_px
    #================================#
    def draw_suggestions(self, surface):
        #--------------------------------#
        core = self.grandparent.core
        #--------------------------------#
        if not core.suggestions.candidates:
            return
        #--------------------------------#
        y = (
            self.parent.console_surface.rect.bottom
        )
        #--------------------------------#
        max_candidates = settings.get("console_max_autocomplete_candidates", 4)
        for i, suggestion in enumerate(core.suggestions.candidates[:max_candidates]):
            #--------------------------------#
            color = (255,255,0) if i == core.suggestions.index-1 else (180,180,180)
            bg_color = (0,0,0,150)
            #--------------------------------#
            text_surface = self.console_font.render(
                suggestion["display"],
                False,
                color,
                bg_color
            )
            #--------------------------------#
            surface.blit(text_surface, (118, y))
            #--------------------------------#
            y += self.console_font.get_height() + 2
    #================================#
    def draw_input(self, surface):
        core = self.grandparent.core
        #--------------------------------#
        y = self.parent.console_surface.input_surface.get_height()//2 + self.parent.console_surface.output_surface.get_height() - self.padding[1] * 2
        #-----------------------#
        if core.text_input.has_selection():
            start, end = sorted([core.text_input.selection_start, core.text_input.selection_end])

            prefix = "> "

            font = self.console_font

            start_x = font.render(prefix + core.text_input.text[:start], False, (0,0,0)).get_width()
            end_x = font.render(prefix + core.text_input.text[:end], False, (0,0,0)).get_width()

            pg.draw.rect(
                surface,
                (settings.get("console_selection_color", [80, 80, 160])),  # cor da seleção
                (
                    self.padding[0] + start_x, #- core.scroll_offset,
                    y,
                    end_x - start_x,
                    font.get_height()
                )
            )
        #--------------------------------#
        visible_surface, cursor_x = self.get_visible_input(
            self.console_font,
            surface.get_width() - self.parent.console_surface.scaled_outline_width - self.parent.console_surface.line_width//2
        )
        #--------------------------------#
        surface.blit(visible_surface, (self.padding[0], y))
        #--------------------------------#
        if pg.time.get_ticks() % 800 < 400:
            #--------------------------------#
            pg.draw.line(
                surface,
                (255,255,255),
                (self.padding[0] + cursor_x, y),
                (self.padding[0] + cursor_x + scaler.constant(1), y + self.console_font.get_height()),
                scaler.constant(1)
            )
    #================================#
    def wrap_text(self, text, font, max_width):
        #--------------------------------#
        words = text.split(" ")
        lines = []
        current = ""
        #--------------------------------#
        for word in words:
            #--------------------------------#
            test_line = current + (" " if current else "") + word
            width = font.render(test_line, False, (0,0,0)).get_width()
            #--------------------------------#
            if width <= max_width:
                current = test_line
            #--------------------------------#
            else:
                #--------------------------------#
                if current:
                    lines.append(current)
                #--------------------------------#
                current = word
        #--------------------------------#
        if current:
            lines.append(current)
        #--------------------------------#
        return lines
    #================================#
    def draw(self, surface, screen):
        self.draw_lines(surface)
        self.draw_input(surface)
        self.draw_suggestions(screen)

