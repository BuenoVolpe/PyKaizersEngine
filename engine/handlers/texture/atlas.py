import pygame as pg
from engine.handlers.texture.texture_data import TextureData
#=====================================#
class TextureAtlas:
    #=====================================#
    def __init__(self):
        self._atlas:dict = {}
    #=====================================#
    def add(self, texture: object):
        self._atlas[texture.resource] = texture
    #=====================================#
    def get(self, resource: str) -> TextureData:
        return self._atlas.get(resource)
    #=====================================#
    def exists(self, resource: str) -> bool:
        return resource in self._atlas
    #=====================================#
    def remove(self, resource: str):
        self._atlas.pop(resource, None)
    #=====================================#
    def clear(self):
        self._atlas.clear()
    #=====================================#
    def __contains__(self, resource: str):
        return resource in self._atlas
    #=====================================#
    def __getitem__(self, resource: str):
        return self._atlas[resource]