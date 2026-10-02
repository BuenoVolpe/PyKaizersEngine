import pygame
from sys import exit
#=====================================#
pygame.init()
#=====================================#
class Game:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self.screen = pygame.display.set_mode([320,180])
        self.clock = pygame.time.Clock()
    #=====================================#
    def run(self):
        #-------------------------------------#
        while True:
            #-------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            #=====================================#
            #game code

            #=====================================#
            pygame.display.update()
            self.clock.tick(60)
#=====================================#
if __name__ == "__main__":
    #-------------------------------------#
    game:Game = Game()
    game.run()
    #-------------------------------------#

