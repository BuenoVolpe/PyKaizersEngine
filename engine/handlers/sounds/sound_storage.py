import os
import pygame as pg
from random import choice
from collections import defaultdict
from engine.configs.paths import paths
from engine.configs.settings import settings
from engine.utils.json import scan_folder
from engine.utils.log import log_error
from engine.console import console

class SoundStorage:

    def __init__(self, audio_paths:dict):
        self.paths = audio_paths

        error_path = paths.get("error_sound", "assets/engine/audio/error.wav")

        self.error = {
            "sound": pg.mixer.Sound(error_path),
            "category": "sfx"
        }

        self.sounds = {}
        self.groups = defaultdict(list)

        for key, path in self.paths.items():
            self._load(path, base=key)

    def _load(self, path, base="pykaizers"):

        for full_path, _ in scan_folder(path, ".wav"):

            rel = os.path.relpath(full_path, path)

            parts = rel.split(os.sep)

            category = parts[0] if len(parts) > 1 else "sfx"
            group = parts[1] if len(parts) > 2 else category

            key = rel.replace(".wav", "").replace("\\", ".")

            data = {
                "sound": pg.mixer.Sound(full_path),
                "category": category
            }

            if base == "pykaizers":
                if category != group:
                    self.groups[f"audio@pyk::group::{category}.{group}"].append(data)
                else:
                    self.groups[f"audio@pyk::group::{group}"].append(data)
                self.sounds[f"audio@pyk::{key}"] = data
            else:
                if category != group:
                    self.groups[f"audio@{base}::group::{category}.{group}"].append(data)
                else:
                    self.groups[f"audio@{base}::group::{group}"].append(data)
                self.sounds[f"audio@{base}::{key}"] = data

    def get(self, key):
        return self.sounds.get(key, self.error)

    def random_from_group(self, group):
        if group not in self.groups:
            log_error(f"group: {group} not in self.groups", console)
            print(self.groups)
            return self.error
        return choice(self.groups[group])
