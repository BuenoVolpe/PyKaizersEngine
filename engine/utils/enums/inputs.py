from engine.configs.inputs import inputs
import pygame as pg
#================================#
class InputsEnum:
    #--------------------------------#
    up = inputs.get("up")
    down = inputs.get("down")
    left = inputs.get("left")
    right = inputs.get("right")
    #--------------------------------#
    menu = inputs.get("menu")
    #--------------------------------#
    LMB = inputs.get("LMB")
    RMB = inputs.get("RMB")
    MMB = inputs.get("MMB")
    #--------------------------------#
    tab = inputs.get("tab")
    #--------------------------------#
    fast_quit = inputs.get("fast_quit")
    restart = inputs.get("restart")
    #--------------------------------#
    #--------------------------------#
    confirm_key = inputs.get("confirm_key")
    alt_key = inputs.get("alt_key")
    #--------------------------------#
    interact = inputs.get("interact", pg.K_e)
#================================#
InputsEnum = InputsEnum()
