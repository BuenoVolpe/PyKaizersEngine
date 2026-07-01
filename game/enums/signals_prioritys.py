#=====================================#
from engine.configs.configs import configs
#=====================================#
mark = configs.engine.asset_marks.signal
pyk = configs.engine.acronym
pykinst = configs.game.acronym
#=====================================#
class SignalsPriority:
    #-------------------------------------#
    FIRST:int = 0
    #-------------------------------------#
    ADD_OBJ:int = 1
    REMOVE_OBJ:int = 1
    #-------------------------------------#
    UPDATE_GLOBAL_OBJ:int = 3
    UPDATE_OBJ:int = 4
    UPDATE_UI:int = 5
    #-------------------------------------#
    SOUND:int = 6
    #-------------------------------------#
    LAST:int = 255
    
#=====================================#
signals_prioritys = SignalsPriority()
sig_prio = signals_prioritys
