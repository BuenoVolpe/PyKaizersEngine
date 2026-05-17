import pygame as pg

class KonamiDetector:
    def __init__(self, input, confirm_key, alt_key):

        self.sequence = [
            input.event_input("up"),
            input.event_input("up"),
            input.event_input("down"),
            input.event_input("down"),
            input.event_input("left"),
            input.event_input("right"),
            input.event_input("left"),
            input.event_input("right"),
            confirm_key,
            alt_key
        ]
        self.progress = 0

    def update(self, event):
        key = None
        if event.type == pg.MOUSEBUTTONDOWN:
            key = event.button
        elif event.type == pg.KEYDOWN:
            key = event.key
        #================================#
        if key == self.sequence[self.progress]:

            self.progress += 1

            if self.progress >= len(self.sequence):
                self.progress = 0
                return True

        else:
            if key is None:
                return False
            self.progress = 0

        return False