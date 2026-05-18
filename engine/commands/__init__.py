from engine.console import command, console
from engine.configs.settings import settings
#-----------------------#
@command("say", protection_level=0)
def say(text:str="hello, world!"):
    """logs and prints a text at the console"""
    return text
@command("close", protection_level=0)
def close():
    """closes console"""
    console.visible = False

@command("change_rendermode", protection_level=4)
def change_rendermode():
    """changes rendermode"""
    console.game.render.render3D = not console.game.render.render3D
    if console.game.render.render3D:
        return "render mode changed to 3D"
    elif console.game.render.render3D:
        return "render mode changed to 2D"





