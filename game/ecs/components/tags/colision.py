from engine.ecs.components import register_game_component
from game.ecs.components.tags import TagComponent
#=====================================#
@register_game_component
class ColisionTag(TagComponent):
    #--------------------------------#
    HAS_COLISION = True
#=====================================#



