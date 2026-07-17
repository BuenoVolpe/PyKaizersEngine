import math
from engine.ecs.components.all import Position, Velocity, GridCollider, Direction, AngularMovementTag, CollisionTag
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
class GridCollisionSystem:
    def __init__(self, world, grid):
        #--------------------------------#
        self.world = world
        self.grid = grid
        #--------------------------------#
        self.map_h = grid
        self.map_w = grid[0]
        #--------------------------------#
        signal_bus.subscribe(signals.GRID_COLLISION_CHANGE_GRID, self.change_grid, priority=sig_prio.AFTER_LOAD)
    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (pos, vel, collider, coltag) in self.world.query(Position, Velocity, GridCollider, CollisionTag, exclude=(AngularMovementTag,)):
            #--------------------------------#
            self.try_move(pos, vel, collider, vel.x * dt, vel.y * dt)
        for entity, (pos, vel, collider, direction, angtag, coltag) in self.world.query(Position, Velocity, GridCollider, Direction, AngularMovementTag, CollisionTag):
            #--------------------------------#
            dx, dy = self._camera_motion(direction, vel)
            self.try_move(pos, vel, collider, dx * dt, dy * dt)
            #--------------------------------#
    #================================#
    def _camera_motion(self, direction, vel):
        #--------------------------------#
        fx = direction.x
        fy = direction.y
        #--------------------------------#
        rx = -fy
        ry = fx
        #--------------------------------#
        forward = -vel.y
        strafe = vel.x
        #--------------------------------#
        dx = fx * forward + rx * strafe
        dy = fy * forward + ry * strafe
        #--------------------------------#
        return dx, dy
    #================================#
    def try_move(self, pos, vel, collider, dx, dy):
        #--------------------------------#
        r = collider.radius
        #--------------------------------#
        nx = pos.x + dx
        if self.is_free(nx, pos.y, r):
            pos.x = nx
        #--------------------------------#
        ny = pos.y + dy
        if self.is_free(pos.x, ny, r):
            pos.y = ny
        #--------------------------------#
    #================================#
    def is_free(self, x, y, r):
        #--------------------------------#
        return self.grid[int(math.floor(x))][int(math.floor(y))] == 0
        # return (
        #     self.is_empty(x-r, y-r) and
        #     self.is_empty(x+r, y-r) and
        #     self.is_empty(x-r, y+r) and
        #     self.is_empty(x+r, y+r)
        # )
    #================================#
    def is_empty(self, x, y):
        tx = int(math.floor(x))
        ty = int(math.floor(y))
        if tx < 0 or ty < 0:
            return False
        if tx >= self.map_w or ty >= self.map_h:
            return False
        return self.grid[ty, tx] == 0
    #================================#
    def change_grid(self, new_grid):
        self.grid = new_grid
        self.map_h = new_grid.shape[0]
        self.map_w = new_grid.shape[1]
    
