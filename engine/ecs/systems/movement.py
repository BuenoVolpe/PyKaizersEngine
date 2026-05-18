from engine.ecs.components.all import Velocity, Position, ColisionTag
from engine.utils.scaler import scaler
#================================#
class SimpleMovementSystem:
    #--------------------------------#
    def __init__(self, world, **kwargs):
        #--------------------------------#
        self.world = world
        for key, value in kwargs.items():
            setattr(self, key, value)
    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (vel, pos) in self.world.query(Velocity, Position, exclude=(ColisionTag, )):
            x, y = vel.x, vel.y
            #--------------------------------#
            pos.x += x * dt
            pos.y += y * dt
            #--------------------------------#
#--------------------------------#


