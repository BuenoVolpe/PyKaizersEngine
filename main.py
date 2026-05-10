import pygame as pg
from sys import exit
#--------------------------------#
import os
import time
#--------------------------------#
from engine.utils.json import json_reader
from engine.utils.scaler import scaler
#--------------------------------#
from engine.configs.settings import settings
from engine.configs.paths import paths
from engine.configs.inputs import inputs
#--------------------------------#
from game.enums.inputs import InputsEnum as Inp
from game.enums.events import events
#--------------------------------#
from engine.utils.event_bus import event_bus
#--------------------------------#
from engine.handlers.sounds import SoundHandler
from engine.handlers.textures import TextureHandler
#--------------------------------#
from game.fonts import AtariSmall, dogicapixel, PixelOperator
#================================#
from game.main.events_handler import EventsHandler
from game.main.display import Display
from game.main.render import Render
from game.main.updater import Updater
#================================#
pg.init()
pg.key.set_repeat(400, 40)
#================================#
class Game:
#================================#
    def __init__(self):
        #================================#
        self.events_handler = EventsHandler()
        self.display = Display()
        self.render = Render()
        self.updater = Updater()
        #================================#
        #--------------------------------#
        self.clock = pg.time.Clock()
        #--------------------------------#
        self.SoundHandler = SoundHandler()
        self.TextureHandler = self.render.TextureHandler
        #--------------------------------#
        pg.display.set_icon(self.TextureHandler.get(settings.get("icon", "pyk::kaizerthrone")))
        #--------------------------------#
        self.prev_time = 0
    #=====================================#
    def run(self):
        #================================#
        while True:
            #----------delta time----------#  
            now = time.time()
            dt = now - self.prev_time
            self.prev_time = now
            #--------------------------------#
            self.events_handler.handle_events()
            #--------------------------------#
            #game code
            event_bus.process()
            self.render.draw(self.display.screen, self.display.main_surface)
            self.updater.update(dt)
            #--------------------------------#
            pg.display.update()
            self.clock.tick(60)
#================================#
if __name__ == "__main__":
    #--------------------------------#
    game = Game()
    #--------------------------------#
    game.run()
#================================#

