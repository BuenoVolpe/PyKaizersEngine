import pygame as pg
#-------------------------------#
from engine.configs.settings import settings
from engine.configs.inputs import inputs
from game.enums.inputs import InputsEnum as Inp
#================================#
class Player:
    #-------------------------------#
    def __init__(self, game, color="standard", nickname="Guest"):
        #-------------------------------#
        self.game = game
        self.nickname = nickname
        #-------------------------------#
        self.TextureHandler = game.TextureHandler
        #-------------------------------#
        self.image = self.TextureHandler.get(f"pyk::dave.{color}")
        self.rect = self.image.get_rect(center=settings.base_window_center)
    #================================#
    def update(self, dt:float = 0):
        #-------------------------------#
        if inputs.input(Inp.up):
            self.rect.y -= 500*dt
        #-------------------------------#
        if inputs.input(Inp.down):
            self.rect.y += 500*dt
        #-------------------------------#
        if inputs.input(Inp.left):
            self.rect.x -= 500*dt
        #-------------------------------#
        if inputs.input(Inp.right):
            self.rect.x += 500*dt
    #================================#
    def draw(self, surface):
        surface.blit(self.image, self.rect)
