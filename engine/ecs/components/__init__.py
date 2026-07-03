import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Texture:
    #--------------------------------#
    def __init__(self, texture:str, scale:tuple=None):
        #--------------------------------#
        self.texture = globalclasses.TextureHandler.get(texture)
        self.scale = scale
#================================#
@register_engine_component
class Position:
    #--------------------------------#
    def __init__(self, x:float, y:float):
        #--------------------------------#
        self.x = x
        self.y = y
        #--------------------------------#
        self.pos = pg.Vector2(x,y)
#================================#

