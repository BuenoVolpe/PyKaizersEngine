#---imports---#
from dataclasses import dataclass
import numpy as np
from engine.configs.configs import configs
#---world map---#
worldMap_list = [
  [8,8,8,8,8,8,8,8,8,8,8,4,4,6,4,4,6,4,6,4,4,4,6,4],
  [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
  [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,6],
  [8,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
  [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
  [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,6,6,6,0,6,4,6],
  [8,8,8,8,0,8,8,8,8,8,8,4,4,4,4,4,4,6,0,0,0,0,0,6],
  [7,7,7,7,0,7,7,7,7,0,8,0,8,0,8,0,8,4,0,4,0,6,0,6],
  [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,0,0,0,0,0,6],
  [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,0,0,0,0,4],
  [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,6,0,6,0,6],
  [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,4,6,0,6,6,6],
  [7,7,7,7,0,7,7,7,7,8,8,4,0,6,8,4,8,3,3,3,0,3,3,3],
  [2,2,2,2,0,2,2,2,2,4,6,4,0,0,6,0,6,3,0,0,0,0,0,3],
  [2,2,0,0,0,0,0,2,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
  [2,0,0,0,0,0,0,0,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
  [1,0,0,0,0,0,0,0,1,4,4,4,4,4,6,0,6,3,3,0,0,0,3,3],
  [2,0,0,0,0,0,0,0,2,2,2,1,2,2,2,6,6,0,0,5,0,5,0,5],
  [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
  [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
  [2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,5,5,5,5,5,5,5,5,5]
]
worldMap = np.array(worldMap_list, dtype=np.int32)
#---settings part 2---#
MAP_H = len(worldMap_list)
MAP_W = len(worldMap_list[0])
#---sprite class---#
@dataclass
class Sprite:
    x: float        #postions
    y: float        #postions
    texture: int    #texture index
#---sprite list---#
sprites = np.array([ #(x, y, texture)
    (20.5, 11.5, 10),
    (18.5, 4.5, 10),
    (10.0, 4.5, 10),
    (10.0, 12.5,10),
    (3.5,  6.5, 10),
    (3.5,  20.5,10),
    (3.5,  14.5,10),
    (14.5,20.5,10),
    (18.5, 10.5, 9),
    (18.5, 11.5, 9),
    (18.5, 12.5, 9),
    (21.5, 1.5, 8),
    (15.5, 1.5, 8),
    (16.0, 1.8, 8),
    (16.2, 1.2, 8),
    (3.5,  2.5, 8),
    (9.5, 15.5, 8),
    (10.0, 15.1,8),
    (10.5, 15.8,8),
], dtype=np.float64)

NUM_SPRITES = sprites.shape[0]

#* x, y, tipo[0v, 1h], espessura, textura, colisão?, twid
# default_thin_walls = np.array([
# ], dtype=np.float64)
# default_thin_walls_data = np.empty((0, 6), dtype=np.float64)
default_thin_walls_data = [
    {
        "pos":[5.0, 7.0],
        "orientation":0,
        "width":1,
        "texture":"raytexture@pyk::raycaster.mine::bricks",
        "colision":True
    }
    # [5.0, 7.0, 0, 1, 8, 1],
    # [20.0, 5.0, 1, 1, 8, 1],
]
# default_thin_walls_data = np.array(default_thin_walls_list, dtype=np.float64)

# default_doors = np.array([
# ], dtype=np.float64)
#* x, y, tipo, largura, tex, offset(qnt abriu), speed, open_state, H?, H_texture, did, eid
# default_doors = np.empty((0, 12), dtype=np.float64)
default_doors = [
    {
        "pos": [20.5, 5.0],
        "orientation": 1,
        "width": 1,
        "tex": "raytexture@pyk::raycaster.mine::pine_door",
        "open_porc": 0,
        "speed": 1,
        "open_state": False, 
        "jamb": True,
        "jamb_texture": "raytexture@pyk::raycaster.mine::pine_planks"
    }
    ]

# --- sprites ---
#* x, y, tex, scale, offsetZ, flags, sid, eid
# default_sprites_data = np.empty((0, 8), dtype=np.float64)
default_sprites_data = [
    {
        "pos":[20.5, 11.5],
        "texture": "raytexture@pyk::raycaster.dave",
        "scale": 0.5,
        "offsetZ": 0.5,
        "flags": 0,
        "sid": -1,
        "eid": -1
    }
    # (20.5, 11.5, 10, .5, .5, 0, 0, -1),
    # (18.5, 4.5, 10, 1, 0, 0, 0, -1),
    # (10.0, 4.5, 10, 1, 0, 0, 0, -1),
    # (10.0, 12.5,10, 1, 0, 0, 0),
    # (3.5,  6.5, 10, 1, 0, 0, 0),
    # (3.5,  20.5,10, 1, 0, 0, 0),
    # (3.5,  14.5,10, 1, 0, 0, 0),
    # (14.5,20.5,10, 1, 0, 0, 0),
    # (18.5, 10.5, 9, 1, 0, 0, 0),
    # (18.5, 11.5, 9, 1, 0, 0, 0),
    # (18.5, 12.5, 9, 1, 0, 0, 0),
    # (21.5, 1.5, 8, 1, 0, 0, 0),
    # (15.5, 1.5, 8, 1, 0, 0, 0),
    # (16.0, 1.8, 8, 1, 0, 0, 0),
    # (16.2, 1.2, 8, 1, 0, 0, 0),
    # (3.5,  2.5, 8, 1, 0, 0, 0),
    # (9.5, 15.5, 8, 1, 0, 0, 0),
    # (10.0, 15.1,8, 1, 0, 0, 0),
    # (10.5, 15.8,8, 1, 0, 0, 0),
]


