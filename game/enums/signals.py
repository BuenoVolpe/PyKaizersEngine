#=====================================#
from engine.configs import configs
#=====================================#
signal = configs.engine.resource_type_marks.signal
seps = configs.engine.resource_strings_seps
pyk = configs.engine.acronym
pykinst = configs.game.acronym
#=====================================#
class Signals:
    #------------------------------------------------------------#
    RENDER_ADD_IMG:str = f"{signal}{seps.type}{pyk}{seps.namespace}render.add.image"
    RENDER_REMOVE_IMG:str = f"{signal}{seps.type}{pyk}{seps.namespace}render.remove.image"
    #------------------------------------------------------------#
    UPDATER_ADD_OBJECT:str = f"{signal}{seps.type}{pyk}{seps.namespace}updater.add.object"
    UPDATER_REMOVE_OBJECT:str = f"{signal}{seps.type}{pyk}{seps.namespace}updater.remove.object"
    #------------------------------------------------------------#
    ENGINE_UPDATE:str = f"{signal}{seps.type}{pyk}{seps.namespace}engine.update"
    #------------------------------------------------------------#
    EVENT_HANDLER_ADD_OBJECT:str = f"{signal}{seps.type}{pyk}{seps.namespace}events_handler.add.object"
    EVENT_HANDLER_REMOVE_OBJECT:str = f"{signal}{seps.type}{pyk}{seps.namespace}events_handler.remove.object"
    #------------------------------------------------------------#
    INPUT:str = f"{signal}{seps.type}{pyk}{seps.namespace}input"
    NO_INPUT:str = f"{signal}{seps.type}{pyk}{seps.namespace}no_input"
    #------------------------------------------------------------#
    PGEVENT:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent"
    PGEVENT_KEYDOWN:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.key.down"
    PGEVENT_KEYUP:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.key.up"
    PGEVENT_MOUSEBUTTONDOWN:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.mouse.down"
    PGEVENT_MOUSEBUTTONUP:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.mouse.up"
    PGEVENT_MOUSEMOTION:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.mouse.motion"
    PGEVENT_MOUSEWHEEL:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.mouse.wheel"
    PGEVENT_MOUSEWHEEL_UP:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.mouse.wheel.up"
    PGEVENT_MOUSEWHEEL_DOWN:str = f"{signal}{seps.type}{pyk}{seps.namespace}pgevent.mouse.wheel.down"
    #------------------------------------------------------------#
    DISPLAY_BUILDED_SCREEN:str = f"{signal}{seps.type}{pyk}{seps.namespace}display.builded_screen"
#=====================================#
signals = Signals()
