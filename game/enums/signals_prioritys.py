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
    AFTER_ADD_OBJ:int = 2
    REMOVE_OBJ:int = 3
    AFTER_REMOVE_OBJ:int = 4
    #-------------------------------------#
    UPDATE_GLOBAL_OBJ:int = 5
    UPDATE_OBJ:int = 6
    UPDATE_UI:int = 7
    #-------------------------------------#
    SOUND:int = 8
    #-------------------------------------#
    LAST:int = 255
    
#=====================================#
signals_prioritys = SignalsPriority()
sig_prio = signals_prioritys
