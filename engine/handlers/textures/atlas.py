from random import choice
from engine.utils.log import log_error
from engine.console import console

class AtlasStorage:
    """
    Stores and manages all loaded sprites.

    Works like a dictionary atlas:
        atlas["player.idle"] -> Surface
    """
    def __init__(self, error_image:object):
        # Dictionary that holds all sprites
        self.data = {}
        self.raycaster_textures_count = 0
        self.raycaster_textures_keys = []
        self.raycaster_textures_id = {}
        self.raycaster_textures = []

        # Fallback sprite if something is missing
        self.error_image = error_image
        self.save("texture@pyk::error", error_image)

    def save(self, name: str, surface:object):
        """
        Saves a sprite into the atlas.
        """
        self.data[name] = surface

    def get_raycaster_texture_path(self, id: int):
        if id-1 > len(self.raycaster_textures_keys)-1:
            log_error(f"id {id} is too big try something between 0 and {len(self.raycaster_textures_keys)-1}", console)
            return "texture@pyk::error" #error
        return self.raycaster_textures_keys[id-1]

    def get_raycaster_texture_id(self, name: str):
        texture = self.raycaster_textures_id.get(name)
        if texture is None:
            log_error(f"texture {name} not found as a raycaster texture, returning error image", console)
            print(self.raycaster_textures_id)
            return 0 #error
        return texture

    def get_raycaster_texture_by_id(self, id: int):
        if id-1 > len(self.raycaster_textures_keys)-1:
            log_error(f"id {id} is too big try something between 0 and {len(self.raycaster_textures_keys)-1}. Returning error texture", console)
            return self.get("texture@pyk::error")
        return self.raycaster_textures[id-1]

    def get(self, name: str):
        """
        Retrieves a sprite safely.

        Returns error sprite if missing.
        """
        if self.data.get(name):
            return self.data[name]
        log_error(f"Sprite '{name}' not found in atlas. Returning error sprite.", console)
        return self.error_image

    def random(self):
        """
        Returns a random sprite from the atlas (debug purpose).
        """
        return choice(list(self.data.values()))

