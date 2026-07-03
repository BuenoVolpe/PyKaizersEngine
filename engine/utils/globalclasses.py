from engine.handlers.textures import TextureHandler
from engine.handlers.audio import AudioHandler
from engine.handlers.fonts import fonts
from engine.signal_bus import SignalBus
#=====================================#
class GlobalClasses:
    TextureHandler:TextureHandler
    AudioHandler:AudioHandler
    fonts = fonts
    #--------------------------------#
    signal_bus:SignalBus
#================================#
globalclasses = GlobalClasses()

