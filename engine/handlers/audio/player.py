import math
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#--------------------------------#
from engine.configs.configs import configs
#--------------------------------#
from engine.utils.log import log
from engine.utils.dict_to_class import dict_to_class
#================================#
from engine.handlers.audio.atlas import Atlas
#================================#
class Player:
    #================================#
    def __init__(self, paths:object, atlas:object):
        #================================#
        self.atlas = atlas
    #================================#
    def play(
        self, name:str, source_pos:tuple|None=None, listener_pos:tuple|None=None, max_distance:float=None, min_distance:float=None,
    ):
        #--------------------------------#
        sound = self.atlas.get(name)
        #--------------------------------#
        channel = sound.play()
        #--------------------------------#
        if channel is None:
            return None
        #--------------------------------#
        #normal sound
        if source_pos is None or listener_pos is None:
            channel.set_volume(1.0, 1.0)
            return channel
        #--------------------------------#
        sx, sy = source_pos
        lx, ly = listener_pos
        #--------------------------------#
        dx = sx - lx
        dy = sy - ly
        #--------------------------------#
        distance = math.hypot(dx, dy)
        #--------------------------------#
        pan = max(-1.0, min(1.0, dx / max_distance))
        left = (1 - pan) / 2
        right = (1 + pan) / 2
        #--------------------------------#
        min_distance = min_distance or 0
        max_distance = max_distance or 0
        volume = 1.0
        #--------------------------------#
        if min_distance and max_distance:
            #--------------------------------#
            if distance <= min_distance:
                volume = 1.0
            #--------------------------------#
            elif distance >= max_distance:
                volume = 0.0
            #--------------------------------#
            else:
                t = (distance - min_distance) / (max_distance - min_distance)
                volume = (1 - t) ** 2
            #--------------------------------#
        channel.set_volume(left * volume, right * volume)
        #--------------------------------#
        return channel
    #================================#
    def play_group(self, group:str, source_pos:tuple|None=None, listener_pos:tuple|None=None, max_distance:float=None,min_distance:float=None,):
        #--------------------------------#
        sound_name = self.atlas.get_from_group(group, return_string_mode=True)
        #--------------------------------#
        self.play(sound_name, 
                  source_pos, listener_pos, max_distance, min_distance
                  )



