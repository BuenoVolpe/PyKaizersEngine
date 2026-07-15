#---imports---#
import math
from engine.raycaster3D.constants import TEX_W, TEX_H
import numpy as np
from numba import njit
#---main render function---#
@njit(fastmath=True)
def render_frame(posX, posY, dirX, dirY, planeX, planeY,
                 worldMap, textures, tex_count,
                 sprites_arr, num_sprites,
                 buffer_out, ZBuffer):
    """
    Renders a full frame:
    1. Floor and ceiling casting
    2. Wall casting
    3. Sprite casting
    """

    h, w = buffer_out.shape  # Frame height and width

    # --- FLOOR AND CEILING CASTING ---
    # Loop through each row of the bottom half of the screen (floor)
    for y in range(h//2 + 1, h):
        # Ray directions for the left and right side of the screen
        rayDirX0 = dirX - planeX
        rayDirY0 = dirY - planeY
        rayDirX1 = dirX + planeX
        rayDirY1 = dirY + planeY

        p = y - h // 2  # Vertical distance from the screen center
        posZ = 0.5 * h  # Camera height

        # Distance from the floor for the current row
        rowDistance = posZ / p

        # Step increments for moving across the floor horizontally
        floorStepX = rowDistance * (rayDirX1 - rayDirX0) / w
        floorStepY = rowDistance * (rayDirY1 - rayDirY0) / w

        # Starting position on the floor
        floorX = posX + rowDistance * rayDirX0
        floorY = posY + rowDistance * rayDirY0

        # Loop through each column
        for x in range(w):
            cellX = int(floorX)
            cellY = int(floorY)
            # Texture coordinates
            tx = int(TEX_W * (floorX - cellX)) & (TEX_W - 1)
            ty = int(TEX_H * (floorY - cellY)) & (TEX_H - 1)

            # Move floor position to the next pixel
            floorX += floorStepX
            floorY += floorStepY

            # Checkerboard pattern for floor texture
            checker = (cellX + cellY) & 1
            floorTexture = 3 if checker == 0 else 4
            ceilingTexture = 6

            # Floor color with darkening effect
            color = textures[floorTexture, ty, tx]
            color = (color >> 1) & 8355711
            buffer_out[y, x] = color

            # Ceiling color
            color = textures[ceilingTexture, ty, tx]
            color = (color >> 1) & 8355711
            buffer_out[h - y - 1, x] = color

    # --- WALL CASTING ---
    for x in range(w):
        # x-coordinate in camera space (-1 left, 1 right)
        cameraX = 2.0 * x / float(w) - 1.0
        # Ray direction for this column
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX

        mapX = int(posX)
        mapY = int(posY)

        # Delta distances
        deltaDistX = 1e30 if rayDirX == 0 else abs(1.0 / rayDirX)
        deltaDistY = 1e30 if rayDirY == 0 else abs(1.0 / rayDirY)

        # Initial distance to the next side of the grid
        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX
        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        # DDA: traverse the grid until hitting a wall
        hit = 0
        side = 0
        while hit == 0:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0  # x-side
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1  # y-side
            if worldMap[mapX, mapY] > 0:
                hit = 1

        # Perpendicular distance to the wall
        perpWallDist = sideDistX - deltaDistX if side == 0 else sideDistY - deltaDistY
        if perpWallDist == 0: perpWallDist = 1e-6

        # Line height to draw
        lineHeight = int(h / perpWallDist)
        drawStart = max(-lineHeight // 2 + h // 2, 0)
        drawEnd = min(lineHeight // 2 + h // 2, h - 1)

        # Wall texture
        texNum = worldMap[mapX, mapY] - 1
        wallX = posY + perpWallDist * rayDirY if side == 0 else posX + perpWallDist * rayDirX
        wallX -= math.floor(wallX)
        texX = int(wallX * TEX_W)
        if (side == 0 and rayDirX > 0) or (side == 1 and rayDirY < 0):
            texX = TEX_W - texX - 1

        # Step in texture
        step = TEX_H / lineHeight
        texPos = (drawStart - h / 2 + lineHeight / 2) * step
        for y in range(drawStart, drawEnd + 1):
            texY = int(texPos) & (TEX_H - 1)
            texPos += step
            color = textures[texNum, texY, texX]
            # Darken the side walls
            if side == 1:
                color = (color >> 1) & 8355711
            buffer_out[y, x] = color

        # Store wall distance in z-buffer
        ZBuffer[x] = perpWallDist

    # --- SPRITE CASTING ---
    # Compute distance of each sprite
    spriteOrder = np.arange(num_sprites, dtype=np.int32)
    spriteDist = np.empty(num_sprites, dtype=np.float64)
    for i in range(num_sprites):
        dx = posX - sprites_arr[i,0]
        dy = posY - sprites_arr[i,1]
        spriteDist[i] = dx*dx + dy*dy

    # Sort sprites from farthest to nearest
    for i in range(num_sprites-1):
        maxidx = i
        for j in range(i+1, num_sprites):
            if spriteDist[j] > spriteDist[maxidx]:
                maxidx = j
        spriteDist[i], spriteDist[maxidx] = spriteDist[maxidx], spriteDist[i]
        spriteOrder[i], spriteOrder[maxidx] = spriteOrder[maxidx], spriteOrder[i]

    # Draw each sprite
    for i in range(num_sprites):
        sx = sprites_arr[spriteOrder[i],0] - posX
        sy = sprites_arr[spriteOrder[i],1] - posY
        invDet = 1.0 / (planeX * dirY - dirX * planeY)
        transformX = invDet * (dirY * sx - dirX * sy)
        transformY = invDet * (-planeY * sx + planeX * sy)
        if transformY <= 0.0001:
            continue

        spriteScreenX = int((w / 2) * (1 + transformX / transformY))
        spriteHeight = abs(int(h / transformY))
        drawStartY = max(-spriteHeight // 2 + h // 2, 0)
        drawEndY = min(spriteHeight // 2 + h // 2, h-1)
        spriteWidth = abs(int(h / transformY))
        drawStartX = max(-spriteWidth // 2 + spriteScreenX, 0)
        drawEndX = min(spriteWidth // 2 + spriteScreenX, w-1)
        texId = int(sprites_arr[spriteOrder[i],2])

        # Draw sprite pixel by pixel
        for stripe in range(drawStartX, drawEndX + 1):
            texX = int(256 * (stripe - (-spriteWidth / 2 + spriteScreenX)) * TEX_W / spriteWidth) // 256
            if transformY > 0 and stripe >= 0 and stripe < w and transformY < ZBuffer[stripe]:
                for y in range(drawStartY, drawEndY + 1):
                    d = (y) * 256 - h * 128 + spriteHeight * 128
                    texY = ((d * TEX_H) // spriteHeight) // 256
                    if 0 <= texY < TEX_H:
                        color = textures[texId, texY, texX]
                        # Ignore transparent pixels
                        if (color & 0x00FFFFFF) != 0:
                            buffer_out[y, stripe] = color

    return
