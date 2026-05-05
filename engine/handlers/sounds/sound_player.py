import math
# from engine.utils.map.colision import check_door_collision

class SoundPlayer:

    def __init__(
        self,
        mixer,
        default_min_radius=2,
        default_max_radius=10
    ):
        self.mixer = mixer
        self.default_min = default_min_radius
        self.default_max = default_max_radius
        self.active = []

    def play(
        self,
        sound_data,
        source_pos=None,
        listener_pos=None,
        listener_dir=None,
        # world=None,
        base_volume=1.0,
        min_radius=None,
        max_radius=None
    ):

        if not sound_data:
            return

        sound = sound_data["sound"]
        category = sound_data["category"]

        min_r = min_radius or self.default_min
        max_r = max_radius or self.default_max

        spatial_volume = 1.0
        left = right = 1.0

        if source_pos and listener_pos and listener_dir:

            sx, sy = source_pos
            lx, ly = listener_pos
            dir_x, dir_y = listener_dir

            dx = sx - lx
            dy = sy - ly

            dist = math.hypot(dx, dy)

            if dist >= max_r:
                return

            if dist <= min_r:
                spatial_volume = 1.0
            else:
                falloff = (dist - min_r) / (max_r - min_r)
                spatial_volume = 1 - falloff

            if dist > 0:
                ndx = dx / dist
                ndy = dy / dist
            else:
                ndx = ndy = 0

            right_x = dir_y
            right_y = -dir_x

            pan = ndx * right_x + ndy * right_y
            pan = max(-1, min(1, pan))

            left = (1 - pan) * 0.5
            right = (1 + pan) * 0.5

            forward_dot = ndx * dir_x + ndy * dir_y

            if forward_dot < 0:
                spatial_volume *= 0.6

            # if world:
            #     if self._is_occluded(world, lx, ly, sx, sy):
            #         spatial_volume *= 0.4

        final_volume = self.mixer.get(
            category,
            base_volume * spatial_volume
        )

        channel = sound.play()

        if channel:
            channel.set_volume(
                final_volume * left,
                final_volume * right
            )

            self.active.append({
                "channel": channel,
                "category": category,
                "base": base_volume * spatial_volume,
                "left": left,
                "right": right
            })

    def _is_occluded(self, world, x1, y1, x2, y2, steps=24):

        for i in range(steps):
            t = i / steps

            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t

            ix = int(x)
            iy = int(y)

            if world.grid[ix, iy] > 0:
                return True

            # if check_door_collision(x, y, world.doorsMap):
            #     return True

            # if self._thin_wall_blocks(x, y, world.thin_walls):
            #     return True

        return False

    # def _thin_wall_blocks(self, px, py, thin_walls):

    #     for i in range(thin_walls.shape[0]):

    #         if thin_walls[i, 5] == 0:
    #             continue

    #         wx = thin_walls[i, 0]
    #         wy = thin_walls[i, 1]
    #         wtype = int(thin_walls[i, 2])
    #         thickness = thin_walls[i, 3]

    #         if wtype == 0:  # vertical
    #             if abs(px - wx) < 0.1:
    #                 if abs(py - wy) < thickness / 2:
    #                     return True
    #         else:  # horizontal
    #             if abs(py - wy) < 0.1:
    #                 if abs(px - wx) < thickness / 2:
    #                     return True

    #     return False

    def refresh_volumes(self):

        alive = []

        for s in self.active:

            ch = s["channel"]

            if not ch.get_busy():
                continue

            vol = self.mixer.get(
                s["category"],
                s["base"]
            )

            ch.set_volume(
                vol * s["left"],
                vol * s["right"]
            )

            alive.append(s)

        self.active = alive

