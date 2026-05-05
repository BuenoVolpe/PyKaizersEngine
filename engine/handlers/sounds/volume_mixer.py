class VolumeMixer:

    def __init__(self, settings):
        self.settings = settings
        self.reload()

    def reload(self):

        self.volumes = {
            "master": self.settings.get("master_volume", 1.0),
            "music": self.settings.get("music_volume", 1.0),
            "sfx": self.settings.get("sfx_volume", 1.0),
        }

    def get(self, category, base=1.0):

        cat = self.volumes.get(category, 1.0)
        master = self.volumes.get("master", 1.0)

        return base * cat * master

    def set(self, category, value):

        value = max(0.0, min(1.0, value))
        self.volumes[category] = value

        self.settings.set(f"{category}_volume", value)

