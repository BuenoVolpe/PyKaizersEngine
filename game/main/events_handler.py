import pygame as pg
#================================#
from engine.utils.log import log, log_error
#--------------------------------#
from engine.signal_bus import signal_bus
#--------------------------------#
from engine.configs.configs import configs
#================================#
class EventsHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        self.objects = {}#priotity[objects]
    #=====================================#
    def _subscribe_functions(self):
        #-------------------------------------#
        signal_bus.subscribe("signal@pyk::events_handler.add.object", self.add_object, priority=10)
        signal_bus.subscribe("signal@pyk::events_handler.remove.object", self.remove_object, priority=10)
    #=====================================#
    def handle_events(self):
        #--------------------------------#
        for event in pg.event.get():
            #--------------------------------#
            if event.type == pg.QUIT or (
                    (event.type == pg.KEYDOWN and event.key == pg.K_LALT)
                    # inputs.input_by_event(event, inp.FAST_QUIT, pg.K_LALT, form="down")
                ):
                #--------------------------------#
                return self.quit()
            #------------------------------#
            elif event.type == pg.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pg.KEYUP:
                self.handle_keyup(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.handle_mouseup(event)
            #------------------------------#
            self.inputs(event)
            self.handle_object_events(event)
        return True
    #================================#
    def inputs(self, event):
        ...
    #================================#
    def handle_object_events(self, event):
        #------------------------------#
        for priority in sorted(self.objects.keys()):
            for obj in self.objects[priority]:
                #------------------------------#
                if hasattr(obj, "handle_event"):
                    obj.handle_event(event)
                    continue
                #------------------------------#
                if hasattr(obj, "handle_events"):
                    obj.handle_events(event)
                    continue
                #------------------------------#
                if hasattr(obj, "events"):
                    obj.events(event)
                    continue
                #------------------------------#
                log_error(f"Object {obj.__class__.__name__} does not have handle_event or handle_events or events method.")
        #------------------------------#
    #================================#
    def handle_keydown(self, event):
        #------------------------------#
        signal_bus.emit("signal@pyk::pgevent.key.down", event=event)
    #================================#
    def handle_keyup(self, event):
        #------------------------------#
        signal_bus.emit("signal@pyk::pgevent.key.up", event=event)
    #================================#
    def handle_mousedown(self, event):
        #------------------------------#
        signal_bus.emit("signal@pyk::pgevent.mouse.down", event=event)
    #================================#
    def handle_mouseup(self, event):
        #------------------------------#
        signal_bus.emit("signal@pyk::pgevent.mouse.up", event=event)
    #=====================================#
    def add_object(self, obj:object, priority:int=0):
        #--------------------------------#  
        if priority not in self.objects:
            self.objects[priority] = []
        #--------------------------------#
        self.objects[priority].append(obj)
    #--------------------------------#
    def remove_object(self, obj:object):
        for priority in self.objects:
            if obj in self.objects[priority]:
                self.objects[priority].remove(obj)
                return
    #================================#
    def quit(self):
        #--------------------------------#
        pg.quit()
        exit()
        return False
#--------------------------------#

