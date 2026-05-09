import pygame as pg
from sys import exit
#--------------------------------#
import os
import time
#--------------------------------#
from engine.utils.json import json_reader
from engine.utils.scaler import scaler
#--------------------------------#
from engine.configs.settings import settings
from engine.configs.paths import paths
from engine.configs.inputs import inputs
#--------------------------------#
from game.enums.inputs import InputsEnum as Inp
#--------------------------------#
from engine.handlers.sounds import SoundHandler
from engine.handlers.textures import TextureHandler
#--------------------------------#
from game.fonts import AtariSmall, dogicapixel, PixelOperator
#================================#
pg.init()
#================================#
class Game:
#================================#
    def __init__(self):
        #--------------------------------#
        self.load_screen()
        self.clock = pg.time.Clock()
        #--------------------------------#
        self.SoundHandler = SoundHandler()
        self.TextureHandler = TextureHandler()
        #--------------------------------#
        pg.display.set_icon(self.TextureHandler.get(settings.get("icon", "pyk::kaizerthrone")))
        #--------------------------------#
        self.prev_time = 0
    #================================#
    def load_screen(self):
        #--------------------------------#
        MIN_RES:tuple = settings.base_window_size
        RES:tuple = settings.window_size
        #--------------------------------#
        if settings.fullscreen:
            #------------------------------#
            os.environ["SDL_VIDEO_CENTERED"] = "1"
            info = pg.display.Info()
            #------------------------------#
            WIDTH:int = info.current_w
            HEIGHT:int = info.current_h
            RES:tuple = (WIDTH, HEIGHT)
            #------------------------------#            
            settings.window_width, settings.window_height = settings.window_size = RES
            settings.window_center = RES[0]//2, RES[1]//2
            #------------------------------#            
            scaler.update()
        #--------------------------------#
        MIN_RES:tuple = settings.base_window_size if settings.resize else RES
        #--------------------------------#
        self.main_surface = pg.Surface(MIN_RES)
        #--------------------------------#
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption(settings.window_title)
        #--------------------------------#
        pg.scrap.init()
    #================================#
    def update(self, delta_time:float):
        #--------------------------------#
        pass
    #================================#
    def draw(self):
        #--------------------------------#
        self.screen.fill(settings.get("bg_color", (30,30,30)))
        self.main_surface.fill(settings.get("bg_color", (30,30,30)))
        #--------------------------------#
        scaled_main_surface = self.main_surface
        #================================#
        self.TextureHandler.blit_random(self.main_surface, (50, 50))
        #================================#
        #================================#
        if settings.resize:
            scaled_main_surface = pg.transform.scale(self.main_surface, settings.window_size)
        #------------------------------#
        AtariSmall.render(scaled_main_surface, (10, 10), f"FPS: {self.clock.get_fps():.0f}", size=30)
        self.screen.blit(scaled_main_surface, (0, 0))
        #------------------------------#
    #================================#
    def run(self):
        #================================#
        while True:
            #----------delta time----------#  
            now = time.time()
            dt = now - self.prev_time
            self.prev_time = now
            #--------------------------------#
            for event in pg.event.get():
                #--------------------------------#
                if event.type == pg.QUIT or (
                    inputs.input_by_event(event, "quit", form="down")
                ):
                    #--------------------------------#
                    exit()
                    pg.quit()
                #--------------------------------#
                # if inputs.input_by_event(event, Inp.toggle_fullscreen, form="down"):
                #     settings.fullscreen = not settings.fullscreen
                #     self.load_screen()
                #--------------------------------#
                if inputs.input_by_event(event, Inp.interact, default_key_value=pg.K_e, form="down"):
                    self.SoundHandler.play("pyk::ui.click")
                elif inputs.input_by_event(event, "q", default_key_value=pg.K_q, form="down"):
                    self.SoundHandler.play_group("pyk::group::sfx.cats")
            #--------------------------------#
            #game code
            self.draw()
            self.update(dt)
            #--------------------------------#
            pg.display.update()
            self.clock.tick()
            # self.clock.tick(60)
#================================#
if __name__ == "__main__":
    #--------------------------------#
    game = Game()
    game.run()
#================================#

