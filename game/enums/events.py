class Events:
    #--------------------------------#
    PLAYER_INTERACT = "event@pyk::player.interact"
    #--------------------------------#
    RELOAD_VOLUMES = "event@pyk::volume.reload"
    #--------------------------------#
    SET_VOLUME = "event@pyk::volume.set"
    PLAY_SOUND = "event@pyk::play.sound"
    PLAY_3D_SOUND = "event@pyk::play.sound.3d"
    PLAY_3D_SOUND_GROUP = "event@pyk::play.sound.group.3d"
    PLAY_SOUND_GROUP = "event@pyk::play.sound.group"
    #--------------------------------#
    ADD_OBJECT_TO_EVENT_HANDLER = "event@pyk::add.object.event"
    REMOVE_OBJECT_FROM_EVENT_HANDLER = "event@pyk::remove.object.event"
    #--------------------------------#
    REMOVE_UI_ELEMENT_FROM_LAYER = "event@pyk::remove.ui_element"
    #--------------------------------#
    REMOVE_OBJECT_FROM_LAYER = "event@pyk::remove.object.layer"
    REMOVE_OBJECT_UPDATE = "event@pyk::remove.object.update"
    #--------------------------------#
    ADD_UI_ELEMENT_TO_LAYER = "event@pyk::add.ui_element"
    #--------------------------------#
    ADD_OBJECT_TO_LAYER = "event@pyk::add.object.layer"
    ADD_OBJECT_UPDATE = "event@pyk::add.object.update"
    #--------------------------------#
    KILL_ENTITY = "event@pyk::ecs.kill"
    SPAWN_ENTITY = "event@pyk::ecs.spawn"
    ENTITY_OVERRIDE = "event@pyk::ecs.override"
    CREATE_WORLD = "event@pyk::ecs.create_world"
    #--------------------------------#
    PAUSE = "event@pyk::pause"
    QUIT_GAME = "event@pyk::game.quit"
    CHANGE_RENDER_3D = "event@pyk::game.change_render"
    CREATE_WORLD_RAYCAST = "event@pyk::game.raycaster.create_world"
    #--------------------------------#

#================================#
events = Events()