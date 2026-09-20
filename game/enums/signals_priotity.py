from engine.configs import configs
#----------------------------------------------#
from game.enums.assetsmarks import assetsmarks
#==============================================#
class SignalsPrioritys:
    #-------------------------------------#
    FIRST:int = 0
    #-------------------------------------#
    PRE_LOAD:int = 1
    LOAD:int = 2
    AFTER_LOAD:int = 3
    #-------------------------------------#
    ADD_OBJ:int = 4
    AFTER_ADD_OBJ:int = 5
    REMOVE_OBJ:int = 6
    AFTER_REMOVE_OBJ:int = 7
    #-------------------------------------#
    UPDATE_GLOBAL_OBJ:int = 8
    UPDATE_OBJ:int = 9
    UPDATE_UI:int = 10
    #-------------------------------------#
    SOUND:int = 11
    #-------------------------------------#
    PRE_LAST:int = 254
    LAST:int = 255
#==============================================#
signals_priority:SignalsPrioritys = SignalsPrioritys()
#----------------------------------------------#