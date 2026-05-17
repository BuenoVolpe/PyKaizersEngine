from engine.console import command, console
from engine.configs.settings import settings
#-----------------------#
from engine.utils.event_bus import event_bus
from game.enums.events import events
#================================#
@command("audio.play", protection_level=1)
def audio(audio:str="audio@pyk::error",
        source_pos=None,
        listener_pos=None,
        listener_dir=None,
        base_volume=1.0,
        min_radius=None,
        max_radius=None
        ):
    """logs and prints a text at the console
        source_pos=None,
        listener_pos=None,
        listener_dir=None,
        base_volume=1.0,
        min_radius=None,
        max_radius=None
        """
    #-----------------------#
    event_bus.emit(events.PLAY_3D_SOUND, 
                name = audio,
                source_pos = source_pos,
                listener_pos = listener_pos,
                listener_dir = listener_dir,
                base_volume = base_volume,
                min_radius = min_radius,
                max_radius = max_radius
                   )
    #-----------------------#
    min_radius = 0 if min_radius is None else min_radius
    max_radius = 0 if max_radius is None else max_radius
    radius = max_radius - min_radius
    #-----------------------#
    return f"playing now {audio} with {base_volume}, radius:{radius}, listener_pos:{listener_pos}, source_pos{source_pos}"


@command("audio.play_3d", protection_level=1)
def audio_3d(group:str="audio@pyk::group::sfx.cats",
        source_pos=None,
        listener_pos=None,
        listener_dir=None,
        base_volume=1.0,
        min_radius=None,
        max_radius=None
        ):
    """logs and prints a text at the console
        source_pos=None,
        listener_pos=None,
        listener_dir=None,
        base_volume=1.0,
        min_radius=None,
        max_radius=None
        """
    #-----------------------#
    event_bus.emit(events.PLAY_3D_SOUND_GROUP, 
                group=group,
                source_pos = source_pos,
                listener_pos = listener_pos,
                listener_dir = listener_dir,
                base_volume = base_volume,
                min_radius = min_radius,
                max_radius = max_radius
                   )
    #-----------------------#
    min_radius = 0 if min_radius is None else min_radius
    max_radius = 0 if max_radius is None else max_radius
    radius = max_radius - min_radius
    #-----------------------#
    return f"playing now a randon audio from group {group} with {base_volume}, radius:{radius}, listener_pos:{listener_pos}, source_pos{source_pos}"

@command("audio.volume.set", protection_level=0)
def audio_volume_set(category="sfx", volume=.5):
    volume = max(volume, 0)
    if volume > 1:
        volume = volume/100
        volume = min(volume, 1)
    #-----------------------#
    event_bus.emit(events.SET_VOLUME, 
                category=category,
                volume=volume,
                   )
    #-----------------------#
    return f"volume in category {category} set to {volume}"

@command("audio.volume.reload", protection_level=0)
def audio_volume_reload():
    event_bus.emit(events.RELOAD_VOLUMES) 
    return f"volume reloaded"


