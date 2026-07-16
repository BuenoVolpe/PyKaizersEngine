import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Ray3DSprite:
    def __init__(self, scale=1.0, offsetZ=0.0):
        self.scale = scale
        self.offsetZ = offsetZ

        self.index = None
