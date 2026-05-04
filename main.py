import pygame as pg
from sys import exit
#===========================#
pg.init()
#===========================#
class Game:
#---------------------------#
    def __init__(self):
        self.screen = pg.display.set_mode((640,360))
        self.clock = pg.time.Clock()
    #---------------------------#
    def run(self):
        #---------------------------#
        while True:
            #---------------------------#
            for event in pg.event.get():
                #---------------------------#
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_LALT
                ):
                    #---------------------------#
                    pg.quit()
                    exit()
            #---------------------------#
            #game code
            #---------------------------#
            pg.display.update()
            self.clock.tick(60)
#===========================#
if __name__ == "__main__":
    #V0.0.0.0
    #---------------------------#
    game = Game()
    game.run()
#===========================#

