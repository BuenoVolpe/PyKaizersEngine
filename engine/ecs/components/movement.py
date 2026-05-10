import pygame as pg
from engine.ecs.components import register_component
#================================#
@register_component
class Velocity:
    #--------------------------------#
    def __init__(self, x:float=0, y:float=0, max_vel:tuple[float]=[float("inf"), float("inf")]):
        #--------------------------------#
        self.x = x
        self.y = y
        self.max_vel = max_vel
        #--------------------------------#

