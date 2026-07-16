from engine.ecs.components.all import Position, Texture, Ray3DDoor
from engine.utils.globalclasses import globalclasses
from engine.signal_bus import signal_bus
from game.enums.signals import signals

class Ray3DDoorSystem:
    def __init__(self, world):
        self.world = world

        signal_bus.subscribe(
            signals.ENTITY_REMOVED,
            self.remove_entity
        )

    def remove_entity(self, entity):
        globalclasses.DoorManager.remove_by_eid(entity)

    def update(self, dt):

        for entity, (position, texture, door) in self.world.query(
            Position,
            Texture,
            Ray3DDoor
        ):

            tex = globalclasses.TextureHandler.get_raytexture_id(
                texture.original_texture
            )

            if door.jamb_texture:
                jamb_tex = globalclasses.TextureHandler.get_raytexture_id(
                    door.jamb_texture
                )
            else:
                jamb_tex = tex

            if door.index is None:

                did = globalclasses.DoorManager.add(
                    position.x,
                    position.y,
                    type=door.type,
                    width=door.width,
                    open_state=door.open_state,
                    tex=tex,
                    open_porc=door.open_porc,
                    speed=door.speed,
                    jamb=door.jamb,
                    jamb_texture=jamb_tex,
                    eid=entity
                )

                door.index = did

            else:

                globalclasses.DoorManager.update_door(
                    door.index,
                    position.x,
                    position.y,
                    type=door.type,
                    width=door.width,
                    tex=tex,
                    open_porc=door.open_porc,
                    speed=door.speed,
                    jamb=door.jamb,
                    jamb_texture=jamb_tex
                )

                