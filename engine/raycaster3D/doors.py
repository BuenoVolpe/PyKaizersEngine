import numpy as np
from dataclasses import dataclass
#================================#
from engine.utils.log import log_error
from engine.utils.globalclasses import globalclasses
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.assets_marks import assetsmarks
from game.enums.signals_prioritys import sig_prio
#================================#
@dataclass
class DoorData:
    x: float
    y: float
    orientation: int
    width: int
    tex: int
    open_porc: float = 0.0
    speed: int = 0
    open_state: float = 0.0
    jamb: int = 0
    jamb_texture: int = 0
    did: int = 0
    eid: int = -1
#================================#
class DoorManager:
    def __init__(self, doors:list[dict]):
        #--------------------------------#
        self.data = np.empty((0,12),dtype=np.float64)
        self.spawn_doors(doors)

    #================================#
    def spawn_doors(self, doors:list[dict]):
        #--------------------------------#
        for door_data in doors:
            #--------------------------------#
            x,y = door_data.get("pos")
            #--------------------------------#
            orientation = door_data.get("orientation", 0)
            width = door_data.get("width", 0)
            tex = door_data.get("tex", 0)
            #--------------------------------#
            open_porc = door_data.get("open_porc", 1)
            speed = door_data.get("speed", False)
            open_state = door_data.get("open_state", False)
            jamb = door_data.get("jamb", False)
            jamb_texture = door_data.get("jamb_texture", 0)
            #--------------------------------#
            if isinstance(jamb_texture, str):
                jamb_texture = globalclasses.TextureHandler.get_raytexture_id(jamb_texture)
            #--------------------------------#
            pos = float(x), float(y)
            orientation = int(orientation)
            width = int(width)
            open_porc = float(open_porc) 
            speed = float(speed) 
            open_state = int(open_state) 
            jamb = int(jamb) 
            jamb_texture = int(jamb_texture)
            #--------------------------------#
            signal_bus.emit(signals.SPAWN_ENTITY,
                name=f"{assetsmarks.engine.entity}::raycaster3D.door", pos=pos, 
                overrides={
                    "component@pyk::Ray3DDoor":{
                        "orientation": orientation,
                        "width": width,
                        "open_porc": open_porc,
                        "speed": speed,
                        "open_state": open_state,
                        "jamb": jamb,
                        "jamb_texture": jamb_texture,
                    },
                    "component@pyk::Texture": {"texture": tex, "do_convert_to_surface": False},
                })
            # return eid

    #================================#
    def set_data(self,array):
        #--------------------------------#
        self.data = array

    #================================#
    def get_array(self):
        return self.data
#================================#