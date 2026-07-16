import pygame as pg
import numpy as np
import time
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Inputs:
    #--------------------------------#
    def __init__(self, inputs:dict):
        #--------------------------------#
        self.inputs = {}
        self.input_cooldown = {}
        self.input_last_time = {}
        #--------------------------------#
        for name, cfg in inputs.items():
            #--------------------------------#
            cooldown = cfg.get("cooldown", 0)
            #--------------------------------#
            self.inputs[name] = False
            self.input_cooldown[name] = cooldown
            self.input_last_time[name] = 0
            #--------------------------------#
            setattr(self, name, False)
    #================================#
    def can_press(self, name):
        #--------------------------------#
        cooldown = self.input_cooldown[name]
        #--------------------------------#
        if cooldown == 0:
            return True
        #--------------------------------#
        now = time.monotonic()
        #--------------------------------#
        if now - self.input_last_time[name] >= cooldown:
            self.input_last_time[name] = now
            return True
        #--------------------------------#
        return False
    #================================#
    def _reload(self):
        for name, value in self.inputs.items():
            setattr(self, name, value)
#================================#