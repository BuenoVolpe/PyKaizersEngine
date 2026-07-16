import numpy as np
from dataclasses import dataclass
#================================#
from engine.utils.log import log_error
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
@dataclass
class DoorData:
    x: float
    y: float
    type: int
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
    #--------------------------------#
    #* x, y, tipo, largura, tex, offset(qnt abriu), speed, open_state, H?, H_texture, did, eid
    DOOR_SIZE = 12
    #================================#
    def __init__(self, doors=None):
        self.next_did = 1
        #--------------------------------#
        if doors is None:
            doors = []
        #--------------------------------#
        self.data = np.array(
            doors,
            dtype=np.float64
        )
        #--------------------------------#
        if self.data.size == 0:
            self.data = np.empty((0, self.DOOR_SIZE), dtype=np.float64)
        #--------------------------------#
        signal_bus.subscribe(
            signals.RAYDOOR_ADD,
            self.add,
            priority=sig_prio.ADD_OBJ

        )
        signal_bus.subscribe(
            signals.RAYDOOR_REMOVE,
            self.remove_by_eid,
            priority=sig_prio.REMOVE_OBJ
        )
        signal_bus.subscribe(
            signals.RAYDOORENT_REMOVE,
            self.remove_door,
            priority=sig_prio.REMOVE_OBJ
        )
        # signal_bus.subscribe(
        #     signals.RAYDEBUG_TOGGLE_DOORSENT_VISIBLE,
        #     self.toggle_doorsent_visible,
        #     priority=sig_prio.UPDATE_OBJJ
        # )
        signal_bus.subscribe(
            signals.RAYENT_UPDATE,
            self.remove_door,
            priority=sig_prio.UPDATE_OBJ
        )
    #================================#
    def add(self, x, y, type, width=1, tex=0, open_porc=0, speed=1, open_state=False, jamb=True, jamb_texture=None, eid=None):
        if eid is None:
            log_error(f"door doesn't have an entity")
            #TODO: auto create entity for door
        #--------------------------------#
        did = self.next_did
        self.next_did += 1
        #--------------------------------#
        if jamb_texture is None:
            jamb_texture = tex #jambs are 2 thin_walls without collision next to the door
        # if jamb:
        #     self.create_jambs(x,y,type, jamb_texture) 
        #--------------------------------#
        sprite = np.array(
            [[x, y, type, width, tex, open_porc, speed, open_state, jamb, jamb_texture, did, eid]],
            dtype=np.float64
        )
        #--------------------------------#
        self.data = np.vstack((self.data, sprite))
        return did
    #================================#
    def remove_door(self, did):
        self.data = self.data[self.data[:,10] != did]
    def remove_by_eid(self, eid):
        self.data = self.data[self.data[:,11] != eid]
    #================================#
    def set_open_porc(self, did, value):
        index = np.where(self.data[:,10] == did)[0]

        if len(index):
            self.data[index[0],5] = value
    def set_open_state(self, did, state):
        index = np.where(self.data[:,10] == did)[0]

        if len(index):
            self.data[index[0],7] = state
    #================================#
    def get_array(self):
        return self.data
    #================================#
    def clear(self):
        self.data = np.empty(
            (0,self.DOOR_SIZE),
            dtype=np.float64
        )
    #================================#
    def update_door(self, did, x, y, type=None, width=None, tex=None, open_porc=None, speed=None, open_state=None, jamb=None, jamb_texture=None, eid=None):
        #--------------------------------#
        index = np.where(self.data[:,10] == did)[0]
        #--------------------------------#
        if len(index) == 0:
            return
        #--------------------------------#
        index = index[0]
        #--------------------------------#
        self.data[index,0] = x
        self.data[index,1] = y
        #--------------------------------#
        if type is not None:
            self.data[index,2] = type
        if width is not None:
            self.data[index,3] = width
        if tex is not None:
            self.data[index,4] = tex
        if open_porc is not None:
            self.data[index,5] = open_porc
        if speed is not None:
            self.data[index,6] = speed
        if open_state is not None:
            self.data[index,7] = open_state
        if jamb is not None:
            self.data[index,8] = jamb
        if jamb_texture is not None:
            self.data[index,9] = jamb_texture
        if eid is not None:
            self.data[index,11] = eid
        #--------------------------------#
    #================================#
    def get_door(self, did):
        #--------------------------------#
        result = self.data[self.data[:,10] == did]
        #--------------------------------#
        if len(result):
            return result[0]
        #--------------------------------#
        return None
    #================================#
    def get_door_by_eid(self, eid):
        #--------------------------------#
        result = self.data[self.data[:,11] == eid]
        #--------------------------------#
        if len(result):
            return result[0]
        #--------------------------------#
        return None
