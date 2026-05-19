import numpy as np
#================================#
from engine.configs.settings import settings
from engine.utils.event_bus import event_bus
from game.enums.events import events
from game.enums.event_priority import event_prioritys
#================================#
from engine.raycaster.hard_coded_maps.original import *
from engine.raycaster.hard_coded_maps.default_map import *
#================================#
class Map:
    #-------------------------#
    def __init__(self, game):
        self.game = game
        #-------------------------#
        self.floorDefaultTex1 = "texture@pyk::raycaster.mine::grass"
        self.floorDefaultTex2 = "texture@pyk::raycaster.mine::grass"
        self.ceilDefaultTex = "texture@pyk::raycaster.mine::pine_planks"
        #-------------------------#
        self.grid = default_world_data
        self.ceil_grid = default_ceil_world_data
        self.floor_grid = default_floor_world_data
        self.doorsMap = default_doors
        self.sprites = default_sprites_data
        #-------------------------#
        self.thin_walls = np.vstack((default_thin_walls, self.build_door_frames(default_doors)))
        #-------------------------#
        event_bus.subscribe(events.CREATE_WORLD_RAYCAST, self.build_map, priority=event_prioritys.ADD)
    #================================#
    def build_map(self, world_data):
        get_texture_id = self.game.TextureHandler.get_raycaster_texture_id
        # get_texture_id(name)
        #-------------------------#
        map_info = world_data.get("map", {})
        #-------------------------#
        self.ceil_grid = map_info.get("ceil_grid", default_ceil_world_data)
        self.ceil_grid = np.array(self.ceil_grid, dtype=np.int32)
        self.grid = map_info.get("grid", default_world_data)
        self.grid = np.array(self.grid, dtype=np.int32)
        self.floor_grid = map_info.get("floor_grid", default_floor_world_data)
        self.floor_grid = np.array(self.floor_grid, dtype=np.int32)
        self.thin_walls = map_info.get("thin_walls", default_thin_walls)
        #-------------------------#
        self.thin_walls = np.array(self.thin_walls, dtype=np.float64)
        self.doorsMap = map_info.get("doorsMap", default_doors)
        self.doorsMap = np.array(self.doorsMap, dtype=np.float64)
        self.thin_walls = np.vstack((self.thin_walls, self.build_door_frames(self.doorsMap)))
        #-------------------------#
        textures = world_data.get("textures")
        if textures:
            #-------------------------#
            self.floorDefaultTex1 = textures.get("floorDefaultTex1", self.floorDefaultTex1)
            self.floorDefaultTex1 = get_texture_id(self.floorDefaultTex1)
            self.floorDefaultTex2 = textures.get("floorDefaultTex2", self.floorDefaultTex2)
            self.floorDefaultTex2 = get_texture_id(self.floorDefaultTex2)
            self.ceilDefaultTex = textures.get("ceilDefaultTex", self.ceilDefaultTex)
            self.ceilDefaultTex = get_texture_id(self.ceilDefaultTex)
            #-------------------------#
            for y, line in enumerate(self.grid):
                for x, value in enumerate(line):
                    if value:
                        name = textures.get(str(value),"texture@pyk::error")
                        texture_id = get_texture_id(name)
                        self.grid[y,x] = texture_id
            #-------------------------#
            for y, line in enumerate(self.ceil_grid):
                for x, value in enumerate(line):
                    if value:
                        name = textures.get(str(value),"texture@pyk::error")
                        texture_id = get_texture_id(name)
                        self.ceil_grid[y,x] = texture_id
            #-------------------------#
            for y, line in enumerate(self.ceil_grid):
                for x, value in enumerate(line):
                    if value:
                        name = textures.get(str(value),"texture@pyk::error")
                        texture_id = get_texture_id(name)
                        self.ceil_grid[y,x] = texture_id
            #-------------------------#
            for wall_index, wall_data in enumerate(self.thin_walls):
                name = textures.get(str(int(self.thin_walls[wall_index, 4])), "texture@pyk::error")
                texture_id = get_texture_id(name)
                self.thin_walls[wall_index, 4] = texture_id
            #-------------------------#
            for door_index, door_data in enumerate(self.doorsMap):
                name = textures.get(str(int(self.doorsMap[door_index, 4])), "texture@pyk::error")
                texture_id = get_texture_id(name)
                self.doorsMap[door_index, 4] = texture_id
            #-------------------------#
        world_data.get("sprites")
    #================================#
    def build_door_frames(self, doors):
        #-------------------------#
        frames = []
        #-------------------------#
        for i in range(doors.shape[0]):
            #-------------------------#
            x, y, t, width, use_H, Htex = doors[i, 0], doors[i, 1], int(doors[i, 2]), doors[i, 3], bool(doors[i, 8]), int(doors[i, 9])
            #-------------------------#            
            if not use_H:
                continue
            #-------------------------#
            offset = 1-width
            #-------------------------#
            if t == 0:  # vertical
                # laterais horizontais
                frames.append([int(x), y-offset/2, 1, 1, Htex, 0])
                frames.append([int(x), y-1+offset/2, 1, 1, Htex, 0])
            #-------------------------#
            else:  # horizontal1
                # laterais verticais
                frames.append([x-offset/2, int(y), 0, 1, Htex, 0])
                frames.append([x+offset/2-1, int(y), 0, 1, Htex, 0])
        #-------------------------#
        if not frames:
            return np.empty((0, settings.get("raycast_thin_walls_array_size", 6)), dtype=np.float64)
        return np.array(frames, dtype=np.float64)

