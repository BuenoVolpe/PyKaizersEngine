#--------------------------------#
import math
import pygame as pg
#=====================================#
from engine.ecs.components.all import Position, Velocity, PlayerTag, RaycasterPlayerTag, CameraFov, CameraSensitivity, ColisionTag
#=====================================#
from engine.configs.inputs import inputs
from engine.configs.settings import settings
from engine.utils.log import log_error
from engine.console import console
#--------------------------------#
from game.enums.inputs import InputsEnum as Inp
#=====================================#
class PlayerInputSystem:
    #--------------------------------#
    def __init__(self, world, **kwargs):
        #--------------------------------#
        self.world = world
        for key, value in kwargs.items():
            setattr(self, key, value)
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        for entity, (pos, vel, tag) in self.world.query(Position, Velocity, PlayerTag):
            #--------------------------------#
            px, py = pos.x, pos.y
            #--------------------------------#        
            if inputs.input(Inp.up):
                vel.y = -vel.max_vel[1]
            elif inputs.input(Inp.down):
                vel.y = vel.max_vel[1]
            else: vel.y = 0
            #--------------------------------#        
            if inputs.input(Inp.left):
                vel.x = -vel.max_vel[0]
            elif inputs.input(Inp.right):
                vel.x = vel.max_vel[0]
            else: vel.x = 0

#--------------------------------#
class RaycastPlayerMouseSystem:
    #--------------------------------#
    def __init__(self, world, **kwargs):
        #--------------------------------#
        self.world = world
        for key, value in kwargs.items():
            setattr(self, key, value)
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        for entity, (pos, vel, fov, sensitivity, tag) in self.world.query(Position, Velocity, CameraFov, CameraSensitivity, RaycasterPlayerTag):
            #--------------------------------#
            dir = fov.dir
            plane = fov.plane
            #--------------------------------#
            mx, my = pg.mouse.get_rel()
            #--------------------------------#
            angle = -mx * sensitivity.sensitivity
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            #--------------------------------#
            old_dir_x = dir.x
            dir.x = dir.x*cos_a - dir.y*sin_a
            dir.y = old_dir_x*sin_a + dir.y*cos_a
            #--------------------------------#
            old_plane_x = plane.x
            plane.x = plane.x*cos_a - plane.y*sin_a
            plane.y = old_plane_x*sin_a + plane.y*cos_a

#--------------------------------#
class RaycastCameraUpdateSystem:
    #--------------------------------#
    def __init__(self, world, **kwargs):
        #--------------------------------#
        self.world = world
        for key, value in kwargs.items():
            setattr(self, key, value)
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        camera = self.game.camera
        #--------------------------------#
        loop_interactions = 0
        for entity, (pos, fov, tag) in self.world.query(Position, CameraFov, RaycasterPlayerTag):
            camera.pos = pos.x, pos.y
            camera.dir = fov.dir.x, fov.dir.y
            camera.plane = fov.plane.x, fov.plane.y
        if loop_interactions >= 1:
            log_error(f"there's more than one player camera. there's {loop_interactions}")

#--------------------------------#
class RaycasterPlayerColisionSystem:
    def __init__(self, world, **kwargs):
        pass
        #--------------------------------#
        self.world = world
        for key, value in kwargs.items():
            setattr(self, key, value)
        #--------------------------------#
        # ceil_grid = self.map.ceil_grid
        # thin_walls = self.map.thin_walls
        # floor_grid = self.map.floor_grid
        # grid = self.map.grid
        # doorsMap = self.map.doorsMap
        # sprites = self.map.sprites
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        for entity, (pos, vel, fov, player_tag, colision_tag) in self.world.query(Position, Velocity, CameraFov, RaycasterPlayerTag, ColisionTag,):
            #--------------------------------#
            if colision_tag.type != "RAYCAST_CAMERA":
                continue
            #--------------------------------#
            px, py = pos.x, pos.y
            dir = fov.dir
            plane = fov.plane        
            #--------------------------------#
            dx, dy = 0,0
            #--------------------------------#
            if inputs.input(Inp.up):
                self.move(dir.x*vel.max_vel[0] * dt, dir.y*vel.max_vel[1] * dt, pos)
            elif inputs.input(Inp.down):
                self.move(-dir.x*vel.max_vel[0] * dt, -dir.y*vel.max_vel[1] * dt, pos)
            #--------------------------------#        
            # vetor lateral (perpendicular)
            right_x = dir.y
            right_y = -dir.x
            #--------------------------------#        
            if inputs.input(Inp.left):
                self.move(-right_x * vel.max_vel[0] * dt, -right_y * vel.max_vel[1] * dt, pos)
            elif inputs.input(Inp.right):
                self.move(right_x * vel.max_vel[0] * dt, right_y * vel.max_vel[1] * dt, pos)
            #--------------------------------#        
    #--------------------------------#
    def move(self, dx, dy, pos):
        #--------------------------------#
        nx = pos.x + dx
        ny = pos.y + dy
        #--------------------------------#
        if not self.is_blocked(nx, pos.y):
            pos.x = nx
        #--------------------------------#
        if not self.is_blocked(pos.x, ny):
            pos.y = ny
    #--------------------------------#
    def is_blocked(self, x, y):
        #--------------------------------#
        if self.map.grid[int(x), int(y)] > 0:
            return True
        #--------------------------------#
        if self.check_thin_collision(x-.5, y-.5, self.map.thin_walls):
            return True
        #--------------------------------#
        if self.check_door_collision(x, y, self.map.doorsMap):
            return True
        #--------------------------------#
        return False
    #--------------------------------#
    def check_thin_collision(self, px, py, thin_walls, radius=0.2):
        for i in range(thin_walls.shape[0]):
            if thin_walls[i, 5] == 0:
                continue  # sem colisão

            wx = thin_walls[i, 0]
            wy = thin_walls[i, 1]
            wtype = int(thin_walls[i, 2])
            thickness = thin_walls[i, 3]

            if wtype == 0:  # vertical
                if abs(px - wx) < 0.1 + radius:
                    if abs(py - wy) < thickness/2 + radius:
                        return True

            else:  # horizontal
                if abs(py - wy) < 0.1 + radius:
                    if abs(px - wx) < thickness/2 + radius:
                        return True

        return False

    def check_door_collision(self, px, py, doors, radius=0.2):
        for i in range(doors.shape[0]):

            x = doors[i, 0]
            y = doors[i, 1]
            wtype = int(doors[i, 2])
            width = doors[i, 3]
            offset = doors[i, 5]
            # door_open = doors[i, 7]

            if wtype == 0:  # vertical (abre pro lado)

                door_x = x + offset

                if abs(px - door_x) < 0.1 + radius:
                    if abs(py - y) < width/2 + radius:
                        if offset <= 1-radius*2:
                            return True

            else:  # horizontal

                door_y = y + offset

                if abs(py - door_y) < 0.1 + radius:
                    if abs(px - x) < width/2 + radius:
                        if offset <= 1-radius*2:
                            return True

        return False

                

