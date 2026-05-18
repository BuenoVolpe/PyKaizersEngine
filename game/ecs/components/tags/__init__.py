from engine.ecs.components import register_game_component
#=====================================#
@register_game_component
class TagComponent:
    #--------------------------------#
    def __init__(self, type:str|None=None):
        #--------------------------------#
        if not type:
            self.type = "NOT_SPECIFIED"
            return
        #--------------------------------#
        self.type = type.upper()