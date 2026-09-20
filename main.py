import pygame as pg
import time
#==============================================#
from game.main.events_handler import EventsHandler
from engine.utils.log import printlog
from engine.configs import configs
#----------------------------------------------#
from engine.handlers.textures import TextureHandler
#----------------------------------------------#
from game.main.renderer import Renderer
from game.main.updater import Updater
from game.main.displayer import Display
#==============================================#
pg.init()
#==============================================#
class Main:
    #==============================================#
    def __init__(self):
        #----------------------------------------------#
        self.display:Display = Display()
        self.clock = pg.time.Clock()
        #----------------------------------------------#
        self.textures_handler:TextureHandler = TextureHandler()
        #----------------------------------------------#
        self.running:bool = True
        self.FPS:int = configs.settings.max_fps
        self.prev_time:int = 0
        #----------------------------------------------#
        self.events_handler:EventsHandler = EventsHandler()
        self.renderer:Renderer = Renderer()
        self.updater:Updater = Updater()
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
            self.renderer.draw(self.display.screen, self.display.main_surface, self.dt)
            #==============================================#
            #update
            self.updater.update(self.dt)
            #==============================================#
            pg.display.flip()
            #----------------------------------------------#
            if configs.settings.show_fps_in_title:
                pg.display.set_caption(f"{configs.game.window_title} | {self.clock.get_fps():.0f}")
            #----------------------------------------------#
            if configs.settings.do_limit_fps:
                self.clock.tick(self.FPS)
            #----------------------------------------------#
            else:
                self.clock.tick()

#==============================================#
if __name__ == "__main__":
    #----------------------------------------------#
    app:Main = Main()
    #----------------------------------------------#
    app.run()

