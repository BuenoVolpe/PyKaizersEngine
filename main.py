import pygame as pg
from sys import exit
import time
#================================#
from game.main.events_handler import EventsHandler
from game.main.update import Updater
from game.main.display import Display
from game.main.render import Render
#================================#
pg.init()
#================================#
class Main:
    #================================#
    def __init__(self):
        #--------------------------------#
        self.screen = pg.display.set_mode([640,360])
        self.clock = pg.time.Clock()
        #--------------------------------#
        self.events_handler = EventsHandler(self)
        self.updater = Updater(self)
        self.render = Render(self)
        self.display = Display(self)
        #--------------------------------#
        self.running:bool = True
        # self.paused:bool = False
        self.time:float = 0
    #================================#
    def get_delta_time(self) -> float:
        self.prev_time = time.time()
        #--------------------------------#
        now = time.time()
        #--------------------------------#
        dt = now - self.prev_time
        self.prev_time = now
        #--------------------------------#
        return dt
        #--------------------------------#
    #================================#
    def get_time(self, delta_time:float) -> float:
        self.time += delta_time
        return self.time
    #================================#
    def main(self):
        self.prev_time = time.time()
        #================================#
        while self.running:  
            #================================#
            dt = self.get_delta_time()
            self.time = self.get_time(dt)
            #================================#
            self.events_handler.events()
            #================================#
            self.updater.update(dt)
            self.render.draw(self.display.main_surface, self.display.screen, dt)
            #================================#
            pg.display.set_caption(f"pykaizersEngine | {self.clock.get_fps():.0f}")
            #================================#
            pg.display.update()
            self.clock.tick(60)

#================================#
if __name__ == "__main__":
    #--------------------------------#
    main = Main()
    main.main()
#================================#


