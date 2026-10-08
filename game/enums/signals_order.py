#=====================================#
class SignalsOrder:
    #------------------------------------------------------------#
    class FIRST:
        FIRST:int=0
        A:int=1
        B:int=2
        C:int=3
        D:int=4
        E:int=5
        F:int=6
        G:int=7
        H:int=8
        I:int=9
        J:int=10
        K:int=11
        L:int=12
        M:int=13
        N:int=14
        O:int=15
        LAST:int=16
    FIRST = FIRST()
    #------------------------------------------------------------#
    class LOAD:
        ZERO:int=16
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    LOAD = LOAD()
    #------------------------------------------------------------#
    class ADDOBJ:
        ZERO:int=32
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    ADDOBJ = ADDOBJ()
    #------------------------------------------------------------#
    class REMOVEOBJ:
        ZERO:int=48
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    REMOVEOBJ = REMOVEOBJ()
    #------------------------------------------------------------#
    class INPUT:
        ZERO:int=64
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    INPUT = INPUT()
    #------------------------------------------------------------#
    class UPDATE_GLOBAL_OBJ:
        ZERO:int=80
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    UPDATE_GLOBAL_OBJ = UPDATE_GLOBAL_OBJ()
    #------------------------------------------------------------#
    class UPDATE_OBJ:
        ZERO:int=96
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    UPDATE_OBJ = UPDATE_OBJ()
    #------------------------------------------------------------#
    # I:int = 112
    # J:int = 128
    # K:int = 144
    # L:int = 160
    # M:int = 176
    # N:int = 192
    # O:int = 208
    # P:int = 224
    # Q:int = 240
    #------------------------------------------------------------#
    class LAST:
        ZERO:int=240
        #------------------------------------------------------------#
        FIRST:int=ZERO+1
        B:int=ZERO+2
        C:int=ZERO+3
        D:int=ZERO+4
        E:int=ZERO+5
        F:int=ZERO+6
        G:int=ZERO+7
        H:int=ZERO+8
        I:int=ZERO+9
        J:int=ZERO+10
        K:int=ZERO+11
        L:int=ZERO+12
        M:int=ZERO+13
        N:int=ZERO+14
        O:int=ZERO+15
        LAST:int=ZERO+16
    LAST = LAST()
    #------------------------------------------------------------#
signals_order = SignalsOrder()
