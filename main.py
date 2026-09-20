import pygame as pg
import time
#==============================================#
from engine.handler.events_handler import EventsHandler
from game.main.renderer import Renderer
#==============================================#
pg.init()
#==============================================#
class Main:
    #==============================================#
    def __init__(self):
        #----------------------------------------------#
        self.screen = pg.display.set_mode((320,180))
        self.clock = pg.time.Clock()
        #----------------------------------------------#
        self.running:bool = True
        self.FPS:int = 60
        self.prev_time:int = 0
        #----------------------------------------------#
        self.events_handler:EventsHandler = EventsHandler()
        self.renderer:Renderer = Renderer()
    #==============================================#
    def get_delta_time(self) -> float:
        #----------------------------------------------#
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        #----------------------------------------------#
        return dt
    #==============================================#
    def run(self):
        #----------------------------------------------#
        while self.running:
            #==============================================#
            self.dt:int = self.get_delta_time()
            #==============================================#
            #events
            events:list = self.events_handler.events(self)
            #==============================================#
            #draws
            self.renderer.draw(self.screen)
            #==============================================#
            #update
            #==============================================#
            pg.display.flip()
            self.clock.tick(self.FPS)

#==============================================#
if __name__ == "__main__":
    #----------------------------------------------#
    app:Main = Main()
    #----------------------------------------------#
    app.run()

