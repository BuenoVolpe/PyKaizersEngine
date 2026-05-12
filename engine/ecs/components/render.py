import pygame as pg
from engine.ecs.components import register_engine_component
#================================#
@register_engine_component
class RenderData:
    #--------------------------------#
    def __init__(self, texture:str, scale:list|None=None):
        #--------------------------------#
        self.texture = texture
        self.scale = scale
#================================#
@register_engine_component
class Position:
    #--------------------------------#
    def __init__(self, x:int, y:int):
        #--------------------------------#
        self.x = x
        self.y = y

