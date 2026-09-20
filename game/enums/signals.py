from engine.configs import configs
#----------------------------------------------#
from game.enums.assetsmarks import assetsmarks
#==============================================#
engine_signal:str = assetsmarks.engine.signal
game_signal:str = assetsmarks.game.signal
class Signals:
    #==============================================#
    #Engine
    ENGINE_UPDATE:str = f"{engine_signal}::engine.update"
    #----------------------------------------------#
    UPDATER_ADD_OBJECT:str = f"{engine_signal}::updater.add.object"
    UPDATER_REMOVE_OBJECT:str = f"{engine_signal}::updater.remove.object"
    #----------------------------------------------#
    RENDERER_ADD_OBJECT:str = f"{engine_signal}::renderer.add.object"
    RENDERER_REMOVE_OBJECT:str = f"{engine_signal}::renderer.remove.object"
    #----------------------------------------------#
    EVENT_HANDLER_ADD_OBJECT:str = f"{engine_signal}::event_handler.add.object"
    EVENT_HANDLER_REMOVE_OBJECT:str = f"{engine_signal}::event_handler.remove.object"
    #----------------------------------------------#
    PGEVENT:str = f"{engine_signal}::pgevent"
    PGEVENT_KEY_DOWN:str = f"{engine_signal}::pgevent.key.down"
    PGEVENT_KEY_UP:str = f"{engine_signal}::pgevent.key.up"
    PGEVENT_MOUSE_DOWN:str = f"{engine_signal}::pgevent.mouse.down"
    PGEVENT_MOUSE_UP:str = f"{engine_signal}::pgevent.mouse.up"
    PGEVENT_MOUSE_MOTION:str = f"{engine_signal}::pgevent.mouse.motion"
    PGEVENT_MOUSE_WHEEL:str = f"{engine_signal}::pgevent.mouse.wheel"
    PGEVENT_MOUSE_WHEEL_UP:str = f"{engine_signal}::pgevent.mouse.wheel.up"
    PGEVENT_MOUSE_WHEEL_DOWN:str = f"{engine_signal}::pgevent.mouse.wheel.down"
    #----------------------------------------------#
    TEXTURE_LOG_ATLAS_DATA:str = f"{engine_signal}::textures.log.atlas_data"
    #----------------------------------------------#
    INPUT:str = f"{engine_signal}::input"
    NO_INPUT:str = f"{engine_signal}::no_input"
    #----------------------------------------------#
    DISPLAY_BUILDED_SCREEN:str = f"{engine_signal}::display.builded_screen"
    #==============================================#
    #Game
#==============================================#
signals:Signals = Signals()
#----------------------------------------------#