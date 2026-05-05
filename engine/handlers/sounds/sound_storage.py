import os
import pygame as pg
from random import choice
from collections import defaultdict
from engine.configs.paths import paths
from engine.configs.settings import settings
from engine.utils.json import scan_folder
from engine.utils.log import log_error

class SoundStorage:

    def __init__(self, base_path):
        self.base_path = base_path

        error_path = paths.get("error_sound", "assets/engine/audio/error.wav")

        self.error = {
            "sound": pg.mixer.Sound(error_path),
            "category": "sfx"
        }

        self.sounds = {}
        self.groups = defaultdict(list)

        self._load()

        print(self.sounds)

    def _load(self):

        for full_path, _ in scan_folder(self.base_path, ".wav"):

            rel = os.path.relpath(full_path, self.base_path)

            parts = rel.split(os.sep)

            category = parts[0] if len(parts) > 1 else "sfx"

            group = parts[1] if len(parts) > 2 else category

            key = rel.replace(".wav", "").replace("\\", ".")

            data = {
                "sound": pg.mixer.Sound(full_path),
                "category": category
            }

            self.sounds[key] = data
            self.groups[group].append(data)
            group

    def get(self, key):
        return self.sounds.get(key, self.error)

    def random_from_group(self, group):
        if group not in self.groups:
            log_error(f"group: {group} not in self.groups", False)
            print(self.groups)
            return self.error
        return choice(self.groups[group])
