from engine.ecs.components.all import Velocity, Position
from engine.utils.scaler import scaler
#================================#
class SimpleMovementSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (vel, pos) in self.world.query(Velocity, Position):
            x, y = vel.x, vel.y
            #--------------------------------#
            pos.x += x * dt
            pos.y += y * dt
            #--------------------------------#
#--------------------------------#


