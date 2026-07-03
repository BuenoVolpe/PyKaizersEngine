from engine.ecs.components.all import Texture, Position
from engine.utils.scaler import scaler

#================================#
class RenderSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.on_screen:bool = False
        self.world = world

    #================================#
    def update(self, surface):
        #--------------------------------#
        for entity, (render, position) in self.world.query(Texture, Position):
            #--------------------------------#
            if isinstance(render.texture, str):
                render.texture = self.world.game.TextureHandler.get(render.texture)
            #--------------------------------#
            if render.scale:
                render.texture = scaler.surface(render.texture, render.scale)
                render.scale = None
            #--------------------------------#
            texture = render.texture
            scale = render.scale
            pos = x, y = position.x, position.y
            #--------------------------------#
            surface.blit(texture, pos)
            #--------------------------------#