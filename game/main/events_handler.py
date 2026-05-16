import pygame as pg
#--------------------------------#
from engine.configs.settings import settings
from engine.configs.inputs import inputs
#--------------------------------#
from engine.utils.event_bus import event_bus
#--------------------------------#
from engine.utils.log import log_error
#--------------------------------#
from engine.console import console
#--------------------------------#
from game.enums.events import events
from game.enums.inputs import InputsEnum as Inp
#================================#
class EventsHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        self.objects = {"console":console}
        #--------------------------------#
        event_bus.subscribe(events.ADD_OBJECT_TO_EVENT_HANDLER, self.add_object, priority=3)
        event_bus.subscribe(events.REMOVE_OBJECT_FROM_EVENT_HANDLER, self.remove_object, priority=3)

    #================================#
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    inputs.input_by_event(event, "quit", form="down")
                ):
                pg.quit()
                exit()
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
            self.handle_object_events(event)
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
        #------------------------------#
        if (inputs.input_by_event(event, "console_hotkey", default_key_value=pg.K_F2, form="down") and 
            settings.get("console_actived", False) and 
            settings.get("console_actived_by_hotkey", False)):
            console.visible = not console.visible
        #------------------------------#
    #================================#
    def handle_keyup(self, event):
        pass
    #================================#
    def handle_mousedown(self, event):
        pass
    #================================#
    def handle_mouseup(self, event):
        pass

#--------------------------------#

