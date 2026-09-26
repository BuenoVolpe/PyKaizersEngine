import pygame as pg
from sys import exit
import time
#============================================================#
from engine.configs import configs
#============================================================#
from engine.resources_string import ResourceStringManager
#============================================================#
from game.global_classes import globalclasses
from game.main.display import Display
# from game.main.loader import Loader
from game.main.pyevents import PyEvents
from game.main.renderer import Renderer
from game.main.updater import Updater
#============================================================#
pg.init()
#============================================================#
class Game:
    #============================================================#
    def __init__(self):
        #------------------------------------------------------------#
        self.running:bool=True
        #------------------------------------------------------------#
        self._load()
        #------------------------------------------------------------#
    #============================================================#
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
        self.resources_string_manager:ResourceStringManager = ResourceStringManager()
        #------------------------------------------------------------#
        self.resources_string_manager.parse("texture@pyk::characters.player$idle::white?scale=0.9&color='blue'&#enabled='false'")
        #------------------------------------------------------------#
        #loader.load()
        globalclasses.display = self.display
        globalclasses.resources_string_manager = self.resources_string_manager
        #------------------------------------------------------------#
        self.screen = self.display.screen
        self.main_surface = self.display.main_surface
        #------------------------------------------------------------#
        self.clock = pg.time.Clock()
        #------------------------------------------------------------#
    #=====================================#
    def get_delta_time(self) -> float:
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        return dt
    #=====================================#
    def pass_time(self, dt:float) -> float:
        self.time += dt * 1000
        return self.time
    #============================================================#
    def run(self):
        #------------------------------------------------------------#
        while self.running:
            #------------------------------------------------------------#
            delta_time = self.get_delta_time()
            #------------------------------------------------------------#
            result:dict = self.pyevents.handle()
            #------------------------------------------------------------#
            #game code
            self.renderer.draw(self.main_surface, self.screen, delta_time)
            self.updater.update(delta_time)
            #------------------------------------------------------------#
            pg.display.flip()
            #------------------------------------------------------------#
            if configs.settings.do_limit_fps:
                self.clock.tick(configs.settings.max_fps)
            else:
                self.clock.tick()
#============================================================#
if __name__ == "__main__":
    #------------------------------------------------------------#
    game:Game = Game()
    game.run()

