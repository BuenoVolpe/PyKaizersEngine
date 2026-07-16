from engine.ecs.components.all import Position, Texture, Ray3DDoor
from engine.utils.globalclasses import globalclasses
from engine.signal_bus import signal_bus
from game.enums.signals import signals
import numpy as np
#================================#
class Ray3DDoorSystem:
    def __init__(self, world):
        #--------------------------------#
        self.world = world
    #================================#
    def update(self,dt):
        #--------------------------------#
        arr = []
        #--------------------------------#
        for eid,(pos,tex,door) in self.world.query(Position, Texture, Ray3DDoor):
            #--------------------------------#
            texture_id = globalclasses.TextureHandler.get_raytexture_id(tex.texture_name)
            #--------------------------------#
            arr.append([
                pos.x,
                pos.y,
                door.orientation,
                door.width,
                texture_id,
                door.open_porc,
                door.speed,
                door.open_state,
                door.jamb,
                door.jamb_texture,
                door.index,
                eid
            ])
            #--------------------------------#
        globalclasses.DoorManager.set_data(
            np.asarray(arr,dtype=np.float64)
        )
#================================#

                