from engine.configs import configs
#==============================================#
game_acronym:str = configs.game.acronym
engine_acronym:str = configs.engine.acronym
marks = configs.engine.asset_marks
#==============================================#
class Marks:
    def __init__(self, acronym:str):
        #----------------------------------------------#
        self.debug:str = f"{marks.debug}@{acronym}"
        self.signal:str = f"{marks.signal}@{acronym}"
        self.texture:str = f"{marks.texture}@{acronym}"
#==============================================#
class AssetsMarks:
    #----------------------------------------------#
    game:Marks = Marks(game_acronym)
    engine:Marks = Marks(engine_acronym)
#==============================================#
assetsmarks:AssetsMarks = AssetsMarks()
#----------------------------------------------#