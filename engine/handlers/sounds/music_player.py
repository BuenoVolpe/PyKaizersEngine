import pygame as pg
import random
import time
import os

class MusicPlayer:

    def __init__(self, mixer, music_path):

        self.mixer = mixer
        self.music_path = music_path

        self.tracks = []
        self.next_time = 0

        self.min_delay = 20
        self.max_delay = 60

        self._scan()

    def _scan(self):

        for root, _, files in os.walk(self.music_path):
            for f in files:
                if f.endswith(".wav") or f.endswith(".ogg"):
                    self.tracks.append(os.path.join(root, f))

    def play_random(self, fade=2000):

        if not self.tracks:
            return

        track = random.choice(self.tracks)

        pg.mixer.music.load(track)
        pg.mixer.music.play(fade_ms=fade)

        self.apply_volume()

        delay = random.uniform(self.min_delay, self.max_delay)
        self.next_time = time.time() + delay

    def update(self):

        if pg.mixer.music.get_busy():
            return

        if time.time() >= self.next_time:
            self.play_random()

    def apply_volume(self):

        vol = self.mixer.get("music", 1.0)
        pg.mixer.music.set_volume(vol)

    # parar com fade
    def stop(self, fade=2000):

        pg.mixer.music.fadeout(fade)

