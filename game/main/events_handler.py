import pygame as pg
from sys import exit
import time
#================================#
from game.main.loader import loader
#================================#
class EventsHandler:
    def __init__(self, main:object):
        #--------------------------------#
        self.objects = [] #[priotity, object]
        self.main = main
    def add_object(self, obj:object, priotity:int):
        #--------------------------------#
        self.objects.append([priotity, obj])
        self.objects.sort(key=lambda x: x[0])
    #================================#
    def events(self):
        #--------------------------------#
        for event in pg.event.get():
            #================================#
            if event.type == pg.QUIT:
                pg.quit()
                self.main.running = False
                quit()
            #================================#
            elif event.type == pg.KEYDOWN:
                self.key_down(event)
            #--------------------------------#
            elif event.type == pg.KEYUP:
                self.key_up(event)
            #--------------------------------#
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_button_down(event)
            #--------------------------------#
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_button_up(event)
            #--------------------------------#
            elif event.type == pg.MOUSEMOTION:
                self.mouse_motion(event)
            #--------------------------------#
            elif event.type == pg.MOUSEWHEEL:
                self.mouse_wheel(event)
        #--------------------------------#
        for index, (priotity, object) in enumerate(self.objects):
            if hasattr(object, "events"):
                object.events(event)
                continue
            if hasattr(object, "handle_events"):
                object.handle_events(event)
                continue
            if hasattr(object, "handle_event"):
                object.handle_event(event)
                continue

    #================================#
    def key_down(self, event):
        ...
    #================================#
    def key_up(self, event):
        ...
    #================================#
    def mouse_button_down(self, event):
        ...
    #================================#
    def mouse_button_up(self, event):
        ...
    #================================#
    def mouse_motion(self, event):
        ...
    #================================#
    def mouse_wheel(self, event):
        ...

