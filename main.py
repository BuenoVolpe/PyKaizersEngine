import pygame as pg
from sys import exit
#=====================================#
from engine.configs import configs
#=====================================#
pg.init()
#=====================================#
class Game:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self.screen = pg.display.set_mode(configs.settings.window_size)
        self.clock = pg.time.Clock()
    #=====================================#
    def run(self):
        #-------------------------------------#
        while True:
            #-------------------------------------#
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            #=====================================#
            #game code

            #=====================================#
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
if __name__ == "__main__":
    #-------------------------------------#
    game:Game = Game()
    game.run()
    #-------------------------------------#

