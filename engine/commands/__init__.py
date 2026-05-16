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





