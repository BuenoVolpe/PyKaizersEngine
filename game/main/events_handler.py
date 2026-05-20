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
from engine.console.konami_detector import KonamiDetector
#--------------------------------#
from game.enums.events import events
from game.enums.inputs import InputsEnum as Inp
from game.enums.event_priority import event_prioritys as priority
from game.enums.interactions import interactions
#================================#
class EventsHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        self.objects = {"console":console}
        self.konami_detector = KonamiDetector(inputs, inputs.event_input("confirm_key"), inputs.event_input("alt_key"))
        #--------------------------------#
        event_bus.subscribe(events.ADD_OBJECT_TO_EVENT_HANDLER, self.add_object, priority=priority.ADD)
        event_bus.subscribe(events.REMOVE_OBJECT_FROM_EVENT_HANDLER, self.remove_object, priority=priority.REMOVE)
        event_bus.subscribe(events.QUIT_GAME, self.quit, priority=priority.LAST)
    #================================#
    def handle_events(self):
        #--------------------------------#
        for event in pg.event.get():
            #--------------------------------#
            if event.type == pg.QUIT or (
                    inputs.input_by_event(event, "quit", form="down")
                ):
                #--------------------------------#
                event_bus.emit(events.QUIT_GAME)
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
            self.console_active(event)
            #------------------------------#
            self.handle_object_events(event)
    #================================#
    def console_active(self, event):
        did_konami = self.konami_detector.update(event)
        if (did_konami or
                (inputs.input_by_event(event, "console_hotkey", pg.K_F2, "up") and settings.get("console_actived_by_hotkey", False))
                ) and settings.get("console_actived", False):
            #------------------------------#  
            if did_konami:
                event_bus.emit(events.PLAY_SOUND_GROUP, group="audio@pyk::group::sfx.console_open", source_pos=(0,0), listener_pos=(0,0))
            #------------------------------#  
            console.visible = not console.visible
            console.core.suggestions.reset()
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
        if inputs.input_by_event(event, Inp.menu, default_key_value=pg.K_ESCAPE, form="down"):
            event_bus.emit(events.PAUSE) 
        #------------------------------#
        if inputs.input_by_event(event, Inp.interact, default_key_value=pg.K_5, form="down"):
            event_bus.emit(events.PLAYER_INTERACT, interaction_type=interactions.DOORS)
        #     for i in range(doors.shape[0]):

        #         dx = camera.pos[0] - doors[i, 0]
        #         dy = camera.pos[1] - doors[i, 1]

        #         if dx*dx + dy*dy < 2.0:
        #             if can_open_door(camera, doors[i]):
        #                 toggle_door(doors, i)
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

#--------------------------------#

