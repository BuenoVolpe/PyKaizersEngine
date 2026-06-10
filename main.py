import pygame as pg
from sys import exit
import time
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
        self.running:bool = True
        self.paused:bool = False
        # self.time:float = 0
    #================================#
    def get_delta_time(self):
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
    def get_time(self, delta_time:float):
        self.time += delta_time
        return time
    #================================#
    def main(self):
        self.prev_time = time.time()
        #================================#
        while self.running:
            #----------delta time----------#  
            dt = self.get_delta_time()
            self.time = self.get_time(dt)
            #--------------------------------#
            for event in pg.event.get():
                #--------------------------------#
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                #--------------------------------#
            #================================#
            #game code


            #================================#
            pg.display.update()
            self.clock.tick(60)

#================================#
if __name__ == "__main__":
    #--------------------------------#
    main = Main()
    main.main()
#================================#


