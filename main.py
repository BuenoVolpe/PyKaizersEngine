import pygame as pg
from sys import exit
#--------------------------------#
import os
import time
import random
#--------------------------------#
from engine.utils.json import json_reader
from engine.utils.log import log
from engine.utils.scaler import scaler
#--------------------------------#
from engine.configs.settings import settings
from engine.configs.paths import paths
from engine.configs.inputs import inputs
#--------------------------------#
from engine.utils.has_server import has_server
from engine.utils.start_server import start_server
#--------------------------------#
from engine.handlers.sounds import sounds
from engine.handlers.textures import TextureHandler
#================================#
from game.server.network import Network
from game.server.packets import read_packet, create_packet
#================================#
from game.enums.inputs import InputsEnum as Inp
from game.enums.packet_type import PacketType
#--------------------------------#
from game.fonts import AtariSmall, dogicapixel, PixelOperator
#--------------------------------#
from game.player import Player
#================================#
pg.init()
#================================#
class Game:
#================================#
    def __init__(self, nickname:str="Player"):
        #--------------------------------#
        self.nickname = nickname
        #--------------------------------#
        self.load_screen()
        self.clock = pg.time.Clock()
        #--------------------------------#
        self.TextureHandler = TextureHandler()
        #--------------------------------#
        pg.display.set_icon(self.TextureHandler.get(settings.get("icon", "pyk::kaizerthrone")))
        #--------------------------------#
        self.prev_time = 0
        #--------------------------------#
        # self.color = random.choice(["standard", "green", "gray", "yellow", "skin", "pink", "blue"])
        self.player = Player(self, "standard")
        #--------------------------------#
        self.net = Network()
        self.packet = {}
        #--------------------------------#
        self.packet_handlers = {
            PacketType.PLAYERS_OUTPUT: self.handle_players_output,
            PacketType.SERVER_FULL: self.handle_server_full
        }
        self.players = {}
    #================================#
    def load_screen(self):
        #--------------------------------#
        MIN_RES:tuple = settings.base_window_size
        RES:tuple = settings.window_size
        #--------------------------------#
        if settings.fullscreen:
            #------------------------------#
            os.environ["SDL_VIDEO_CENTERED"] = "1"
            info = pg.display.Info()
            #------------------------------#
            WIDTH:int = info.current_w
            HEIGHT:int = info.current_h
            RES:tuple = (WIDTH, HEIGHT)
            #------------------------------#            
            settings.window_width, settings.window_height = settings.window_size = RES
            settings.window_center = RES[0]//2, RES[1]//2
            #------------------------------#            
            scaler.update()
        #--------------------------------#
        MIN_RES:tuple = settings.base_window_size if settings.resize else RES
        #--------------------------------#
        self.main_surface = pg.Surface(MIN_RES)
        #--------------------------------#
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption(settings.window_title)
        #--------------------------------#
        pg.scrap.init()
    #================================#
    def handle_players_output(self, packet):
        #--------------------------------#
        self.players = packet["data"]
    #================================#
    def handle_server_full(self, packet):
        #--------------------------------#
        log("\n\nServer is full!", "CYAN", ["bright"])
    #================================#
    def process_packets(self):
        with self.net.queue_lock:
            packets = self.net.packet_queue.copy()
            self.net.packet_queue.clear()
            for packet in packets:
                handler = self.packet_handlers.get(packet["type"])
                if handler:
                    handler(packet)
    #================================#
    def update(self, dt:float):
        #--------------------------------#
        self.player.update(dt)
        #--------------------------------#
        data = {"pos": [self.player.rect.x, self.player.rect.y], "dir": [0, 0], "nickname": self.nickname, "color":"standard"}
        self.packet = self.net.send(data, packet_type=PacketType.PLAYERS_INPUT)
        #--------------------------------#
    #================================#
    def draw(self):
        #--------------------------------#
        self.screen.fill(settings.get("bg_color", (30,30,30)))
        self.main_surface.fill(settings.get("bg_color", (30,30,30)))
        #================================#
        self.TextureHandler.blit_random(self.main_surface, (50, 50))
        #================================#
        self.player.draw(self.main_surface)
        #------------------------------#        
        for player_id, player_data in self.players.items():
            #--------------------------------#
            if int(player_id) == self.net.id:
                continue
            #--------------------------------#
            player_pos = player_data["pos"]
            player_color = player_data["color"]
            player_image = self.TextureHandler.get(f"pyk::dave.{player_color}")
            self.main_surface.blit(player_image, player_pos)
            #--------------------------------#
        #================================#
        if settings.resize:
            scaled_main_surface = pg.transform.scale(self.main_surface, settings.window_size)
        #------------------------------#
        AtariSmall.render(scaled_main_surface, (10, 10), f"FPS: {self.clock.get_fps():.0f}", size=30)
        self.screen.blit(scaled_main_surface, (0, 0))
        #------------------------------#
    #================================#
    def run(self):
        #================================#
        while True:
            #----------delta time----------#  
            now = time.time()
            dt = now - self.prev_time
            self.prev_time = now
            #--------------------------------#
            for event in pg.event.get():
                #--------------------------------#
                if event.type == pg.QUIT or (
                    inputs.input_by_event(event, "quit", form="down")
                ):
                    #--------------------------------#
                    self.net.disconnect()
                    pg.quit()
                    exit()
                #--------------------------------#
                # if inputs.input_by_event(event, Inp.toggle_fullscreen, form="down"):
                #     settings.fullscreen = not settings.fullscreen
                #     self.load_screen()
                #--------------------------------#
                if inputs.input_by_event(event, Inp.interact, default_key_value=pg.K_e, form="down"):
                    # sounds.play("pyk::ui.click")
                    print(self.nickname)
                elif inputs.input_by_event(event, "q", default_key_value=pg.K_q, form="down"):
                    # sounds.play_group("pyk::group::sfx.cats")
                    print(self.net.id, self.net.role)
            #--------------------------------#
            #game code
            self.process_packets()
            self.update(dt)
            self.draw()
            #--------------------------------#
            pg.display.update()
            # self.clock.tick()
            self.clock.tick(60)
#================================#
if __name__ == "__main__":
    #--------------------------------#
    if not has_server():
        start_server()
    #--------------------------------#
    game = Game(nickname="Player")
    game.run()
#================================#

