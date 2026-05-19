import numpy as np
from engine.utils.event_bus import event_bus
from game.enums.events import events
from game.enums.event_priority import event_prioritys
from engine.configs.settings import settings
# --- mapa---
default_world_data = np.array([
    [1 ,1,2,3,4,1],
    [16,0,0,0,0,5],
    [15,0,0,0,0,6],
    [14,0,0,0,0,7],
    [13,0,0,0,0,8],
    [1,12,11,10,9,1]
], dtype=np.int32)

default_ceil_world_data = np.array([
    [1,1,1,1,1,1],
    [1,0,0,0,0,1],
    [1,1,1,1,1,1],
    [1,2,2,2,2,1],
    [1,3,3,3,3,1],
    [1,1,1,1,1,1]
], dtype=np.int32)

default_floor_world_data = np.array([
    [1,1,1,1,1,1],
    [1,0,0,0,0,1],
    [1,1,1,1,1,1],
    [1,2,2,2,2,1],
    [1,3,3,3,3,1],
    [1,1,1,1,1,1]
], dtype=np.int32)

#* x, y, tipo[0v, 1h], espessura, textura, colisão?
# default_thin_walls = np.array([
# ], dtype=np.float64)
default_thin_walls = np.empty((0, settings.get("raycast_thin_walls_array_size", 6)), dtype=np.float64)

# default_doors = np.array([
# ], dtype=np.float64)
#* x, y, tipo, largura, tex, offset(qnt abriu), speed, open_state, H?, H_texture
default_doors = np.empty((0, settings.get("raycast_thin_doors_array_size", 10)), dtype=np.float64)

# --- sprites ---
# default_sprites_data = np.array([
# ], dtype=np.float64)
#* x, y, tex, scale, offsetZ, flags
default_sprites_data = np.empty((0, settings.get("raycast_thin_sprites_array_size", 6)), dtype=np.float64)

