import pygame as pg
import time
from sys import exit
#=====================================#
from engine.configs import configs
#=====================================#
from game.main.display import Display
from game.main.pyevents import PyEvents
from game.main.renderer import Renderer
from game.main.updater import Updater
#=====================================#
pg.init()
#=====================================#
class Game:
    #=====================================#
    def __init__(self):
        self._load()
        #------------------------------------------------------------#
    def _load(self):
        #------------------------------------------------------------#
        self.prev_time:int = 0 
        self.time:int = 0 
        #------------------------------------------------------------#
        self.display:Display= Display()
        self.pyevents:PyEvents= PyEvents()
        # self.loader:Loader= Loader()
        self.renderer:Renderer= Renderer()
        self.updater:Updater= Updater()
        #------------------------------------------------------------#
        self.screen = self.display.screen
        self.main_surface = self.display.main_surface
        #------------------------------------------------------------#
        self.clock = pg.time.Clock()
    #=====================================#
    def get_delta_time(self) -> float:
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        return dt
    #-------------------------------------#
    def pass_time(self, dt:float) -> float:
        self.time += dt * 1000
        return self.time
    #=====================================#
    def display_update(self):
        #-------------------------------------#
        pg.display.update()
        #-------------------------------------#
        if configs.settings.show_fps_in_title:
            pg.display.set_caption(f"{configs.game.window_title} | {self.clock.get_fps():.0f}")
        #-------------------------------------#
        if configs.settings.do_limit_fps:
            self.clock.tick(configs.settings.max_fps)
        #-------------------------------------#
        else:
            self.clock.tick()
    #=====================================#
    def run(self):
        #-------------------------------------#
        while True:
            #-------------------------------------#
            results:dict = self.pyevents.handle()
            #-------------------------------------#
            delta_time:float = self.get_delta_time()
            self.pass_time(delta_time)
            #-------------------------------------#
            self.updater.update(delta_time=delta_time)
            self.renderer.draw(self.main_surface, self.screen, delta_time=delta_time)
            #=====================================#
            self.display_update()
#=====================================#
if __name__ == "__main__":
    #-------------------------------------#
    game:Game = Game()
    game.run()
    #-------------------------------------#

