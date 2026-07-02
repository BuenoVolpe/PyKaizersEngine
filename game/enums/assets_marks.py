from engine.configs.configs import configs

#=====================================#
class AssetsMarks:
    def __init__(self):
        self.engine = self.Engine()
        self.game = self.Game()
    #=====================================#
    class Engine:
        #-------------------------------------#
        texture:str = f"{configs.engine.asset_marks.texture}@{configs.engine.acronym}"
        audio:str = f"{configs.engine.asset_marks.audio}@{configs.engine.acronym}"
        debug:str = f"{configs.engine.asset_marks.debug}@{configs.engine.acronym}"
        music:str = f"{configs.engine.asset_marks.music}@{configs.engine.acronym}"
        audiogroup:str = f"{configs.engine.asset_marks.audiogroup}@{configs.engine.acronym}"
        signal:str = f"{configs.engine.asset_marks.signal}@{configs.engine.acronym}"
    #=====================================#
    class Game:
        #-------------------------------------#
        texture:str = f"{configs.engine.asset_marks.texture}@{configs.game.acronym}"
        audio:str = f"{configs.engine.asset_marks.audio}@{configs.game.acronym}"
        debug:str = f"{configs.engine.asset_marks.debug}@{configs.game.acronym}"
        music:str = f"{configs.engine.asset_marks.music}@{configs.game.acronym}"
        audiogroup:str = f"{configs.engine.asset_marks.audiogroup}@{configs.game.acronym}"
        signal:str = f"{configs.engine.asset_marks.signal}@{configs.game.acronym}"
#=====================================#
assetsmarks = AssetsMarks()
