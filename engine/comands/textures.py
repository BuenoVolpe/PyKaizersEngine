from engine.console import command, console
from engine.configs.configs import configs
from engine.signal_bus import signal_bus
from game.enums.signals import signals
#-----------------------#
@command("textures.log.atlas_data")
def AUDIO_LOG_ATLAS_DATA():
    signal_bus.emit(signals.TEXTURE_LOG_ATLAS_DATA)