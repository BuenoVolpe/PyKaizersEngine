from engine.ecs.components import register_game_component
#=====================================#
@register_game_component
class PlayerTag:
    IS_PLAYER = True

