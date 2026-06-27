import pygame as pg
import time
from sys import exit
#=====================================#
from game.main.display import Display
from game.main.loader import Loader
from game.main.updater import Updater
from game.main.render import Render
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
        #=====================================#
        self.screen = self.display.screen
        self.main_surface = self.display.main_surface
        #=====================================#

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
        while True:
            #-------------------------------------#
            dt = self.get_delta_time()
            #-------------------------------------#
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_LALT):
                    pg.quit()
                    exit()
            #-------------------------------------#
            self.updater.update(dt)
            self.render.draw(self.screen, self.main_surface, dt)
            #-------------------------------------#
            pg.display.update()
            self.clock.tick(60)

#=====================================#
if __name__ == "__main__":
    main = Main()
    main.run()

