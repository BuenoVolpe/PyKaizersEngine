
from engine.ecs.components.all import Position, Texture, Ray3DSprite
from engine.utils.globalclasses import globalclasses
from engine.utils.scaler import scaler
from engine.signal_bus import signal_bus
#--------------------------------#
import pygame as pg
import math
#--------------------------------#
from game.enums.signals import signals
#================================#
class Ray3DSpriteSystem:
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        signal_bus.subscribe(
            signals.ENTITY_REMOVED,
            self.remove_entity
        )
    #================================#
    def remove_entity(self, entity):
        globalclasses.SpriteManager.remove_entity(entity)
    #================================#
    def update(self, dt, *args, **kwargs):
        #--------------------------------#
        for entity, (position, texture, sprite) in self.world.query(Position,Texture,Ray3DSprite):
            #--------------------------------#
            tex_id = globalclasses.TextureHandler.get_raytexture_id(
                texture.original_texture
            )
            #--------------------------------#
            if sprite.index is None:
                #--------------------------------#
                sid = globalclasses.SpriteManager.add(
                    position.x,
                    position.y,
                    tex_id,
                    sprite.scale,
                    sprite.offsetZ,
                    globalclasses.SpriteManager.SPRITE_ENTITY,
                    entity
                )
                #--------------------------------#
                sprite.index = sid
            #--------------------------------#
            else:
                #--------------------------------#
                globalclasses.SpriteManager.update_entity(
                    sprite.index,
                    position.x,
                    position.y,
                    tex_id,
                    sprite.scale,
                    sprite.offsetZ
                )

                