import pygame as pg
import time
from sys import exit
#=====================================#
from game.main.display import Display
from game.main.events_handler import EventsHandler
from game.main.loader import Loader
from game.main.updater import Updater
from game.main.render import Render
#=====================================#
from engine.configs.configs import configs
#=====================================#
pg.init()
#=====================================#
class Main:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self._load()
    #=====================================#
    def _load(self):
        #-------------------------------------#
        self.clock = pg.time.Clock()
        #=====================================#
        self.prev_time = 0
        #=====================================#
        self.display:Display = Display()
        self.loader:Loader = Loader()
        self.updater:Updater = Updater()
        self.render:Render = Render()
        self.events_handler:EventsHandler = EventsHandler()
        #=====================================#
        self.screen = self.display.screen
        self.main_surface = self.display.main_surface
        #=====================================#
        self.running = True
        #-------------------------------------#
    #=====================================#
    def get_delta_time(self) -> float:
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        return dt
    #=====================================#
    def run(self):
        #=====================================#
        while self.running:
            #-------------------------------------#
            dt = self.get_delta_time()
            #-------------------------------------#
            self.running = self.events_handler.handle_events()
            #-------------------------------------#
            self.updater.update(dt)
            self.render.draw(self.screen, self.main_surface, dt)
            #-------------------------------------#
            if configs.settings.show_fps_in_title:
                pg.display.set_caption(f"{configs.game.window_title} | {self.clock.get_fps():.1f}")
            #-------------------------------------#
            pg.display.update()
            self.clock.tick(configs.settings.max_fps)

#=====================================#
if __name__ == "__main__":
    main = Main()
    main.run()

