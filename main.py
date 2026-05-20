import pygame as pg
from sys import exit
import numpy as np
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
from game.enums.event_priority import event_prioritys
#--------------------------------#
from engine.utils.event_bus import event_bus
#--------------------------------#
from engine.handlers.sounds import SoundHandler
from engine.handlers.textures import TextureHandler
#--------------------------------#
from engine.ecs import World
from engine.ecs.entity_factory import EntityFactory
from engine.ecs.world_factory import WorldFactory
from engine.ecs.components.all import *
#--------------------------------#
from engine.console import console
from engine.commands.all import *
#--------------------------------#
from engine.raycaster.renderer import RaycasterRenderer
from engine.raycaster.doors import update_doors
from engine.raycaster.map import Map
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
        console.game = self
        #================================#
        self.world = World(self)
        self.events_handler = EventsHandler()
        self.display = Display()
        self.render = Render(self.world)
        #-------------------------#
        self.render.map = Map(self)
        #-------------------------#
        self.updater = Updater(self.world, self)
        self.entity_factory = EntityFactory(self.world, self)
        self.world_factory = WorldFactory(self.world, self.entity_factory, self)
        #================================#
        # self.entity_factory.create_entities()
        self.world_factory.create_world("world@pyk::raycaster.exemple")
        #================================#
        self.clock = pg.time.Clock()
        #--------------------------------#
        self.SoundHandler = SoundHandler()
        self.TextureHandler = self.render.TextureHandler
        #--------------------------------#
        pg.display.set_icon(self.TextureHandler.get(settings.get("icon", "texture@pyk::kaizerthrone")))
        #--------------------------------#
        self.prev_time = 0
        event_bus.subscribe(events.CHANGE_RENDER_3D, self._on_change_rendermode, priority=event_prioritys.SIMPLE_RESPONSE)
    #=====================================#
    def _on_change_rendermode(self, **kwargs):
        #--------------------------------#
        if not self.render.render3D:
            return
        #--------------------------------#
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        #--------------------------------#
        self.render.raycast = RaycasterRenderer(self, *self.display.main_surface.get_size())
        self.render.textures_array = self.TextureHandler.atlas.raycaster_textures
        #--------------------------------#
        class Camera:
            player_id = 0
            pos = np.array((22, 11.5), dtype=np.float64)
            dir = np.array((-1,0), dtype=np.float64)
            plane = np.array((0,0.66), dtype=np.float64)
            # set_fov(-90)
        self.camera = Camera()
        #--------------------------------#
        self.render.camera = self.camera

    #=====================================#
    def run(self):
        #--------------------------------#
        self.prev_time = time.time()
        #================================#
        while True:
            #----------delta time----------#  
            now = time.time()
            dt = now - self.prev_time
            self.prev_time = now
            #--------------------------------#
            self.events_handler.handle_events()
            # if not pg.mouse.get_focused():
            #     self.updater.pause = True
            #--------------------------------#
            #game code
            event_bus.process()
            self.updater.update(dt)
            if settings.get("show_fps_on_title", False):
                pg.display.set_caption(f"{settings.window_title} | {self.clock.get_fps():.0f}")
            self.render.draw(self.display.screen, self.display.main_surface)
            self.world.flush()
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

