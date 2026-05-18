class Events:
    #--------------------------------#
    PLAYER_INTERACT = "pyk::player.interact"
    #--------------------------------#
    RELOAD_VOLUMES = "pyk::volume.reload"
    #--------------------------------#
    SET_VOLUME = "pyk::volume.set"
    PLAY_SOUND = "pyk::play.sound"
    PLAY_3D_SOUND = "pyk::play.sound.3d"
    PLAY_3D_SOUND_GROUP = "pyk::play.sound.group.3d"
    PLAY_SOUND_GROUP = "pyk::play.sound.group"
    #--------------------------------#
    ADD_OBJECT_TO_EVENT_HANDLER = "pyk::add.object.event"
    REMOVE_OBJECT_FROM_EVENT_HANDLER = "pyk::remove.object.event"
    #--------------------------------#
    REMOVE_UI_ELEMENT_FROM_LAYER = "pyk::remove.ui_element"
    #--------------------------------#
    REMOVE_OBJECT_FROM_LAYER = "pyk::remove.object.layer"
    REMOVE_OBJECT_UPDATE = "pyk::remove.object.update"
    #--------------------------------#
    ADD_UI_ELEMENT_TO_LAYER = "pyk::add.ui_element"
    #--------------------------------#
    ADD_OBJECT_TO_LAYER = "pyk::add.object.layer"
    ADD_OBJECT_UPDATE = "pyk::add.object.update"
    #--------------------------------#
    KILL_ENTITY = "pyk::ecs.kill"
    SPAWN_ENTITY = "pyk::ecs.spawn"
    ENTITY_OVERRIDE = "pyk::ecs.override"
    CREATE_WORLD = "pyk::ecs.create_world"
    #--------------------------------#
    PAUSE = "pyk::pause"
    QUIT_GAME = "pyk::game.quit"
    CHANGE_RENDER_3D = "pyk::game.change_render"
    #--------------------------------#

#================================#
events = Events()