#=====================================#
from engine.ecs.components.all import Position, Velocity, PlayerTag
#=====================================#
from engine.configs.inputs import inputs
from engine.configs.settings import settings
#--------------------------------#
from game.enums.inputs import InputsEnum as Inp
#=====================================#
class PlayerInputSystem:
    #--------------------------------#
    def __init__(self, world):
        #--------------------------------#
        self.world = world
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
                




