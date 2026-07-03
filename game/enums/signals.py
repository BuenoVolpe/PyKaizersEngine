#=====================================#
from engine.configs.configs import configs
#=====================================#
mark = configs.engine.asset_marks.signal
pyk = configs.engine.acronym
pykinst = configs.game.acronym
#=====================================#
class Signals:
    #-------------------------------------#
    RENDER_ADD_UI_ELEMENT:str = F"{mark}@{pyk}::render.add.ui_element"
    RENDER_REMOVE_UI_ELEMENT:str = F"{mark}@{pyk}::render.remove.ui_element"
    RENDER_ADD_OBJ:str = F"{mark}@{pyk}::render.add.object"
    RENDER_REMOVE_OBJ:str = F"{mark}@{pyk}::render.remove.object"
    RENDER_ADD_IMG:str = F"{mark}@{pyk}::render.add.image"
    RENDER_REMOVE_IMG:str = F"{mark}@{pyk}::render.remove.image"
    #-------------------------------------#
    UPDATER_ADD_OBJECT:str = f"{mark}@{pyk}::updater.add.object"
    UPDATER_REMOVE_OBJECT:str = f"{mark}@{pyk}::updater.remove.object"
    #-------------------------------------#
    ENGINE_UPDATE:str = f"{mark}@{pyk}::engine.update"
    #-------------------------------------#
    EVENT_HANDLER_ADD_OBJECT:str = f"{mark}@{pyk}::events_handler.add.object"
    EVENT_HANDLER_REMOVE_OBJECT:str = f"{mark}@{pyk}::events_handler.remove.object"
    #-------------------------------------#
    ADD_TO_OVERLAY:str = f"{mark}@{pyk}::debug_overlay.add"
    ACTIVE_DEBUGOVERLAY:str = f"{mark}@{pyk}::debug_overlay.active"
    #-------------------------------------#
    PGEVENT:str = f"{mark}@{pyk}::pgevent"
    PGEVENT_KEY_DOWN:str = f"{mark}@{pyk}::pgevent.key.down"
    PGEVENT_KEY_UP:str = f"{mark}@{pyk}::pgevent.key.up"
    PGEVENT_MOUSE_DOWN:str = f"{mark}@{pyk}::pgevent.mouse.down"
    PGEVENT_MOUSE_UP:str = f"{mark}@{pyk}::pgevent.mouse.up"
    #-------------------------------------#
    DISPLAY_BUILDED_SCREEN:str = f"{mark}@{pyk}::display.builded_screen"
    #-------------------------------------#
    SOUND_PLAY:str = f"{mark}@{pyk}::sound.play"
    SOUND_PLAY_GROUP:str = f"{mark}@{pyk}::sound.play.group"
    #-------------------------------------#
    KILL_ENTITY:str = f"{mark}@{pyk}::ecs.entity.kill"
    CREATE_ENTITY:str = f"{mark}@{pyk}::ecs.entity.create"
    ADD_COMPONENT:str = f"{mark}@{pyk}::ecs.component.add"
    REMOVE_COMPONENT:str = f"{mark}@{pyk}::ecs.component.remove"
#=====================================#
signals = Signals()
