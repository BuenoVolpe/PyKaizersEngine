#---imports---#
import math
from engine.raycaster3D.constants import TEX_W, TEX_H
import numpy as np
import pygame
#---auxiliar functions---#
def load_texture(path):
    """
    Loads an image as a texture:
    - converts to a uint32 array in the format 0xRRGGBB
    """
    surf = pygame.image.load(path).convert_alpha()      # carrega imagem com alfa
    surf = pygame.transform.scale(surf, (TEX_W, TEX_H))  # redimensiona
    arr = pygame.surfarray.pixels3d(surf).copy()        # array (w,h,3)
    arr = np.transpose(arr, (1,0,2)).astype(np.uint8)  # para (h,w,3)
    rgb32 = (arr[:,:,0].astype(np.uint32) << 16) | \
            (arr[:,:,1].astype(np.uint32) << 8) | \
            arr[:,:,2].astype(np.uint32)
    return rgb32

def buffer_to_surface(buffer_uint32):
    """
    Convert uint32 buffer (0xRRGGBB) to Pygame Surface
    """
    r = ((buffer_uint32 >> 16) & 0xFF).astype(np.uint8)
    g = ((buffer_uint32 >> 8) & 0xFF).astype(np.uint8)
    b = (buffer_uint32 & 0xFF).astype(np.uint8)
    rgb = np.dstack((r,g,b))
    rgb_t = np.transpose(rgb, (1,0,2))  # Pygame espera (w,h,3)
    surf = pygame.surfarray.make_surface(rgb_t)
    return surf
