import pygame as pg
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#--------------------------------#
from engine.configs.configs import configs
#--------------------------------#
from engine.utils.log import log, log_list, log_dict
from engine.utils.dict_to_class import dict_to_class
#================================#
from engine.handlers.audio.atlas import Atlas
from engine.handlers.audio.loader import Loader
from engine.handlers.audio.player import Player
#================================#
class AudioHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        self.paths = dict_to_class({
            "error": configs.paths.audio_error,
            configs.engine.acronym: configs.paths.engine_audio,
            configs.game.acronym: configs.paths.game_audio,
        })
        #--------------------------------#
        self.atlas = Atlas(self.paths.error)
        self.player = Player(self.paths, self.atlas)
        self.loader = Loader(self.paths, self.atlas)
        self.loader._load()
        #================================#
        signal_bus.subscribe(signals.SOUND_PLAY, self.play, priority=signals_prioritys.SOUND)
        signal_bus.subscribe(signals.SOUND_PLAY_GROUP, self.play_group, priority=signals_prioritys.SOUND)
        #================================#
        # log_list(list(self.atlas.data.keys()))
        # log_dict(self.atlas.groups_data, key_color="WHITE", dict_name="Audio Groups")
        # log_list(list(self.atlas.music_data.keys()), list_name="Music")
    #================================#
    def play(self, sound:str, **kwargs):    
        #--------------------------------#
        self.player.play(sound, **kwargs)
    #================================#
    def play_group(self, sound:str, **kwargs):    
        #--------------------------------#
        self.player.play_group(sound, **kwargs)
