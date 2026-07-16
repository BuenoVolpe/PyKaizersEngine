from engine.ecs.components.all import Camera3D, Direction, Angle, MouseSentibility
from engine.utils.scaler import scaler
import pygame as pg
import math
#================================#
class Raycaster3DCameraSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for ent, (angle, direction, camera) in self.world.query(Angle, Direction, Camera3D):
            #--------------------------------#
            rad = math.radians(angle.angle)

            direction.x = math.cos(rad)
            direction.y = math.sin(rad)
            #--------------------------------#
            plane_len = math.tan(math.radians(camera.fov) / 2)

            camera.plane.x = -direction.y * plane_len
            camera.plane.y = direction.x * plane_len
#================================#
class MouseLookSystem:
    #--------------------------------#
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        pg.mouse.get_rel()
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        dx, dy = pg.mouse.get_rel()
        #--------------------------------#
        for ent, (angle, sens) in self.world.query(Angle,MouseSentibility):
            #--------------------------------#
            angle.angle += dx * sens.sentibility
            #--------------------------------#
            angle.angle %= 360        
#================================#

