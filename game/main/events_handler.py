import pygame as pg
#================================#
from engine.utils.log import log, log_error
#================================#
from engine.configs.configs import configs
#================================#
class EventsHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        self.objects = {}#name:obj
    #================================#
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
        for obj in self.objects.values():
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
    def add_object(self, object_id:str, obj):
        #------------------------------#
        self.objects[object_id] = obj
        #------------------------------#
    def remove_object(self, object_id:str):
        #------------------------------#
        if object_id in self.objects:
            del self.objects[object_id]
        #------------------------------#
    #================================#
    def handle_keydown(self, event):
        pass
    #================================#
    def handle_keyup(self, event):
        pass
    #================================#
    def handle_mousedown(self, event):
        pass
    #================================#
    def handle_mouseup(self, event):
        pass
    #================================#
    def quit(self):
        #--------------------------------#
        pg.quit()
        exit()
        return False
#--------------------------------#

