from engine.utils.event_bus import event_bus
from game.enums.events import events
#--------------------------------#
from engine.configs.paths import paths
from engine.configs.settings import settings
#--------------------------------#
from engine.handlers.sounds.sound_player import SoundPlayer
from engine.handlers.sounds.sound_storage import SoundStorage
from engine.handlers.sounds.volume_mixer import VolumeMixer
from engine.handlers.sounds.music_player import MusicPlayer
#================================#
class SoundHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        audio_paths = {
            "pykaizers": paths.get("engine_audio", "assets/audio/sfx"),
            f"{settings.game_acronym}": paths.get("game_audio", "assets/audio/music")
        }
        #--------------------------------#
        self.mixer = VolumeMixer(settings)
        self.storage = SoundStorage(audio_paths)
        self.player = SoundPlayer(self.mixer)
        self.music = MusicPlayer(
            self.mixer,
            paths.get("music", "assets/audio/music")
        )
        #----------------------------#
        self._apply_initial_volumes()
        #----------------------------#
        event_bus.subscribe(events.PLAY_SOUND, self.play, priority=1)
        event_bus.subscribe(events.PLAY_3D_SOUND, self.play, priority=1)
        event_bus.subscribe(events.PLAY_SOUND_GROUP, self.play_group, priority=1)
        event_bus.subscribe(events.PLAY_3D_SOUND_GROUP, self.play_group, priority=1)
        event_bus.subscribe(events.RELOAD_VOLUMES, self.reload_volumes, priority=1)
        event_bus.subscribe(events.SET_VOLUME, self.set_volume, priority=1)
    #================================#
    def _apply_initial_volumes(self):
        #--------------------------------#
        self.mixer.reload()
        #--------------------------------#
        self.player.refresh_volumes()
        self.music.apply_volume()
    #================================#
    def play(self, name, **kwargs):
        #--------------------------------#
        data = self.storage.get(name)
        #--------------------------------#
        self.player.play(data, **kwargs)
    #================================#
    def play_group(self, group, **kwargs):
        #--------------------------------#
        data = self.random_from_group(group)
        # print(f"Playing sound from group '{group}': {data}")
        #--------------------------------#
        self.player.play(data, **kwargs)
    #================================#
    def random_from_group(self, group):
        #--------------------------------#
        data = self.storage.random_from_group(group)
        #--------------------------------#
        return data
    #================================#
    def reload_volumes(self):
        #--------------------------------#
        self.mixer.reload()
    #================================#
    def update(self):
        #--------------------------------#
        self.music.update()
    #================================#
    def set_volume(self, category, volume):
        #--------------------------------#
        self.mixer.set(category, volume)
        #--------------------------------#
        self.player.refresh_volumes()
        #--------------------------------#
        if category == "music":
            self.music.apply_volume()
#================================#
# normal sound
# sounds.play("audio@pyk::ui.click")

# spacial sound
# sounds.play(
#     "audio@pyk::ui.click",
#     source_pos=enemy.pos,
#     listener_pos=player.pos
# )

# group sound
# sounds.play_group(
#     "audio@pyk::group::sfx.cats",
#     source_pos=cat.pos,
#     listener_pos=player.pos
# )

# volume
# sounds.mixer.set_master(0.6)
# sounds.mixer.set_category("music", 0.2)
# music only
# sounds.music.apply_volume()

# music
# sounds.music.play_random()
# sounds.music.stop()

# sound_handler.set_volume("sfx", 0.2)
# sound_handler.set_volume("music", 0.5)
# sound_handler.set_volume("master", 1.0)

