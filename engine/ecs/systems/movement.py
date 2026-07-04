from engine.ecs.components.all import Velocity, Position
from engine.utils.scaler import scaler

#================================#
class MovementSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.on_screen:bool = False
        self.world = world

    #================================#
    def update(self, surface):
        #--------------------------------#
        for entity, (velocity, position) in self.world.query(Velocity, Position):
            #--------------------------------#
            position.x += velocity.x
            position.y += velocity.y
