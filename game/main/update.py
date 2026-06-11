import pygame as pg
from sys import exit
import time
#================================#
from game.main.loader import loader
#================================#
class Updater:
    #================================#
    def __init__(self, main:object):
        #--------------------------------#
        self.systems = loader._load_updater_systems()
        #--------------------------------#
        self.objects = [] #[priotity, object]
        self.main = main
    #================================#
    def add_object(self, obj:object, priotity:int):
        #--------------------------------#
        self.objects.append([priotity, obj])
        self.objects.sort(key=lambda x: x[0])
    #================================#
    def update(self, delta_time:float):
        #--------------------------------#
        for index, system in enumerate(self.systems):
            system.update(delta_time)
        #--------------------------------#
        for index, object in enumerate(self.objects):
            if hasattr(object, "update"):
                object.update(delta_time)
        #--------------------------------#
    #================================#



