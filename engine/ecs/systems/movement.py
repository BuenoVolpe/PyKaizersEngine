from engine.ecs.components.all import Velocity, Position, AngularMovementTag, Angle
from engine.utils.scaler import scaler
import math
#================================#
class MovementSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (velocity, position) in self.world.query(Velocity, Position, exclude=(AngularMovementTag, )):
            #--------------------------------#
            position.x += velocity.x * dt
            position.y += velocity.y * dt
            #
            # --------------------------------#
            position.pos.update(
                position.x,
                position.y
            )
#================================#
class AngularMovementSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for entity, (velocity, position, angle, tag) in self.world.query(Velocity, Position, Angle, AngularMovementTag):
            #--------------------------------#
            direction_x = math.cos(math.radians(angle.angle))
            direction_y = math.sin(math.radians(angle.angle))
            #--------------------------------#
            position.x += direction_x * velocity.x * dt
            position.y += direction_y * velocity.x * dt
            #--------------------------------#
            position.pos.update(
                position.x,
                position.y
            )
            
