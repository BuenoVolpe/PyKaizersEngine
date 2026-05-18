import pygame as pg
import math
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
#================================#
@register_engine_component
class CameraDirection:
    #--------------------------------#
    def __init__(self, x:float, y:float):
        #--------------------------------#
        self.x = x
        self.y = y
        
@register_engine_component        
class CameraPlane:
    #--------------------------------#
    def __init__(self, x:float, y:float):
        #--------------------------------#
        self.x = x
        self.y = y

@register_engine_component        
class CameraFov:
    def __init__(self, angle, camera_plane:list=(0,0.66), camera_dir:list=(-1,0)):
        #--------------------------------#
        self.plane = CameraPlane(*camera_plane)
        self.dir = CameraDirection(*camera_dir)
        #--------------------------------#
        self.set_fov(angle)
    
    #--------------------------------#
    def set_fov(self, fov_degrees):
        #--------------------------------#
        fov_rad = math.radians(fov_degrees)
        plane_length = math.tan(fov_rad / 2)
        #--------------------------------#
        self.plane.x = -self.dir.y * plane_length
        self.plane.y = self.dir.x * plane_length

@register_engine_component        
class CameraSensitivity:
    def __init__(self, sensitivity:float=0.002):
        self.sensitivity = sensitivity
