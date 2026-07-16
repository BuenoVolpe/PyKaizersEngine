import numpy as np
from dataclasses import dataclass
#================================#
from engine.signal_bus import signal_bus
from engine.utils.globalclasses import globalclasses
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
@dataclass
class SpriteData:
    x: float
    y: float
    tex: int
    scale: float = 1.0
    offsetZ: float = 0.0
    flags: int = 0
    sid: int = 0
    eid: int = -1
#================================#
class SpriteManager:
    #--------------------------------#
    SPRITE_NORMAL = 0
    SPRITE_ENTITY = 1
    # SPRITE_ITEM = 2
    # SPRITE_ENEMY = 4
    #--------------------------------#
    # x,y,tex,scale,offsetZ,flags,sid
    SPRITE_SIZE = 8
    #================================#
    def __init__(self, sprites:list[dict]=None):
        self.next_sid = 1
        self.data = np.empty((0, self.SPRITE_SIZE), dtype=np.float64)
        #--------------------------------#
        if sprites:
            self._load(sprites)
        #--------------------------------#
        signal_bus.subscribe(
            signals.RAYSPRITE_ADD,
            self.add,
            priority=sig_prio.ADD_OBJ

        )
        signal_bus.subscribe(
            signals.RAYSPRITE_REMOVE,
            self.remove,
            priority=sig_prio.REMOVE_OBJ
        )
        signal_bus.subscribe(
            signals.RAYSPRITEENT_REMOVE,
            self.remove_entity,
            priority=sig_prio.REMOVE_OBJ
        )
        signal_bus.subscribe(
            signals.RAYSPRITEENT_UPDATE,
            self.update_entity,
            priority=sig_prio.UPDATE_OBJ
        )
    #================================#
    def add(self, x, y, tex, scale=1.0, offsetZ=0.0, flags=0, eid=-1):
        #--------------------------------#
        sid = self.next_sid
        self.next_sid += 1
        #--------------------------------#
        sprite = np.array(
            [[x,y,tex,scale,offsetZ,flags,sid,eid]],
            dtype=np.float64
        )
        #--------------------------------#
        self.data = np.vstack((self.data, sprite))
        return sid
    #================================#
    def remove(self, sid):
        self.data = self.data[self.data[:,6] != sid]
    def remove_entity(self, eid):
        self.data = self.data[self.data[:,7] != eid]
    #================================#
    def get_array(self):
        return self.data
    #================================#
    def clear(self):
        self.data = np.empty(
            (0,self.SPRITE_SIZE),
            dtype=np.float64
        )
    #================================#
    def update_entity(self, sid, x, y, tex=None, scale=None, offsetZ=None):
        #--------------------------------#
        index = np.where(self.data[:,6] == sid)[0]
        #--------------------------------#
        if len(index) == 0:
            return
        #--------------------------------#
        index = index[0]
        #--------------------------------#
        self.data[index,0] = x
        self.data[index,1] = y
        #--------------------------------#
        if tex is not None:
            self.data[index,2] = tex
        #--------------------------------#
        if scale is not None:
            self.data[index,3] = scale
        #--------------------------------#
        if offsetZ is not None:
            self.data[index,4] = offsetZ
    #================================#
    def _load(self, sprites):
        #--------------------------------#
        for sprite_data in sprites:
            #--------------------------------#
            x,y = sprite_data.get("pos")
            tex = sprite_data.get("texture")
            #--------------------------------#
            if isinstance(tex, str):
                tex = globalclasses.TextureHandler.get_raytexture_id(tex)
            #--------------------------------#
            scale = sprite_data.get("scale", 1.0)
            offsetZ = sprite_data.get("offsetZ", 0.0)
            flags = sprite_data.get("flags", 0)
            eid = sprite_data.get("eid", -1)
            #--------------------------------#
            self.add(
                x,y,
                tex,
                scale,
                offsetZ,
                flags,
                eid
                )


    #================================#
    def get_sprite(self, sid):
        #--------------------------------#
        result = self.data[self.data[:,6] == sid]
        #--------------------------------#
        if len(result):
            return result[0]
        #--------------------------------#
        return None

