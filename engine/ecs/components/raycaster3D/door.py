import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Ray3DDoor:
    def __init__(self, orientation=0, width=1, open_porc=0, speed=1, open_state=True, jamb=True, jamb_texture=None):
        #--------------------------------#
        self.orientation = orientation
        self.width = width
        #--------------------------------#
        self.open_porc = open_porc
        self.speed = speed
        self.open_state = open_state
        #--------------------------------#
        self.jamb = jamb
        self.jamb_texture = jamb_texture
        #--------------------------------#
        self.index = None
#================================#
