import pygame as pg


def recolor (image:pg.Surface, color_map:dict):
    img = image.copy()
    px = pg.PixelArray(img)

    for src, dst in color_map.items():
        px.replace(src, dst[:3])

    del px
    return img

def darken_color(color, factor=0.7):
    r, g, b = color
    r = min(max(int(r * factor), 0), 255)
    g = min(max(int(g * factor), 0), 255)
    b = min(max(int(b * factor), 0), 255)
    return (r, g, b)

def apply_multi_colorkey(surface, colors):
    surface = surface.convert_alpha()
    width, height = surface.get_size()

    for x in range(width):
        for y in range(height):
            color = surface.get_at((x, y))[:3]
            if color in colors:
                surface.set_at((x, y), (0, 0, 0, 0))

    return surface
