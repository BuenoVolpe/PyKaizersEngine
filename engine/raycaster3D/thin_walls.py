import numpy as np
from dataclasses import dataclass
#================================#
from engine.utils.log import log_error
from engine.utils.globalclasses import globalclasses
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
class ThinWallsManager:
    #--------------------------------#
    #* x, y, tipo[0v, 1h], espessura, textura, colisão?, twid
    THIN_WALL_SIZE = 7
    #================================#
    def __init__(self, thin_walls:list[dict]=None):
        self.next_twid = 1
        self.data = np.empty((0, self.THIN_WALL_SIZE), dtype=np.float64)
        #--------------------------------#
        if thin_walls:
            self._load(thin_walls)
        #--------------------------------#
        signal_bus.subscribe(
            signals.RAYTW_ADD,
            self.add,
            priority=sig_prio.ADD_OBJ
        )
        signal_bus.subscribe(
            signals.RAYTW_REMOVE,
            self.remove_wall,
            priority=sig_prio.REMOVE_OBJ
        )
        signal_bus.subscribe(
            signals.RAYTW_UPDATE,
            self.update_thin_wall,
            priority=sig_prio.REMOVE_OBJ
        )
    #================================#
    def add(self, x, y, orientation, width=0, texture=0, colision=True):
        #--------------------------------#
        twid = self.next_twid
        self.next_twid += 1
        # --------------------------------#
        sprite = np.array(
            [[
                float(x), float(y),
                int(orientation), 
                float(width),
                int(texture), 
                int(colision), 
                int(twid), 
            ]],
            dtype=np.float64
        )
        # --------------------------------#
        self.data = np.vstack((self.data, sprite))
        return twid
    #================================#
    def remove_wall(self, twid):
        self.data = self.data[self.data[:,6] != twid]
    #================================#
    def get_array(self):
        return self.data
    #================================#
    def clear(self):
        self.data = np.empty(
            (0,self.THIN_WALL_SIZE),
            dtype=np.float64
        )
    #================================#
    def _load(self, thin_walls:list[dict]):
        #--------------------------------#
        for thin_wall_data in thin_walls:
            #--------------------------------#
            x,y = thin_wall_data.get("pos")
            #--------------------------------#
            orientation = thin_wall_data.get("orientation")
            width = thin_wall_data.get("width", 1)
            texture = thin_wall_data.get("texture")
            colision = thin_wall_data.get("colision", True)
            #--------------------------------#
            if isinstance(texture, str):
                texture = globalclasses.TextureHandler.get_raytexture_id(texture)
            #--------------------------------#
            self.add(x, y, orientation, width, texture, colision)
    #================================#
    def update_thin_wall(self, twid, x, y, orientation=None, width=None, tex=None, colision=None):
        #--------------------------------#
        index = np.where(self.data[:,6] == twid)[0]
        #--------------------------------#
        if len(index) == 0:
            return
        #--------------------------------#
        index = index[0]
        #--------------------------------#
        self.data[index,0] = x
        self.data[index,1] = y
        #--------------------------------#
        if orientation is not None:
            self.data[index,2] = orientation
        if width is not None:
            self.data[index,3] = width
        if tex is not None:
            self.data[index,4] = tex
        if colision is not None:
            self.data[index,5] = colision
        #--------------------------------#
    #================================#
    def get_thin_wall(self, twid):
        #--------------------------------#
        result = self.data[self.data[:,10] == twid]
        #--------------------------------#
        if len(result):
            return result[0]
        #--------------------------------#
        return None
    #================================#
