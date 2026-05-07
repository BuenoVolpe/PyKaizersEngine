from random import choice
from engine.utils.log import log_error

class AtlasStorage:
    """
    Stores and manages all loaded sprites.

    Works like a dictionary atlas:
        atlas["player.idle"] -> Surface
    """
    def __init__(self, error_image:object):
        # Dictionary that holds all sprites
        self.data = {}

        # Fallback sprite if something is missing
        self.error_image = error_image

    def save(self, name: str, surface:object):
        """
        Saves a sprite into the atlas.
        """
        self.data[name] = surface

    def get(self, name: str):
        """
        Retrieves a sprite safely.

        Returns error sprite if missing.
        """
        if self.data.get(name):
            return self.data[name]
        log_error(f"Sprite '{name}' not found in atlas. Returning error sprite.")
        print("Available sprites:", list(self.data.keys()))
        return self.error_image

    def random(self):
        """
        Returns a random sprite from the atlas (debug purpose).
        """
        return choice(list(self.data.values()))

