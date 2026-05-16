from engine.console import command, console
from engine.configs.settings import settings
#------------------------#
from engine.utils.log import log, log_success
#------------------------#
@command("test.protection_level_0", protection_level=0)
def z():
    return "you have acess to commands with protection level 0 (simple commands)"
@command("test.protection_level_1", protection_level=1)
def a():
    return "you have acess to commands with protection level 1 (simple cheats)"
@command("test.protection_level_2", protection_level=2)
def b():
    return "you have acess to commands with protection level 2 (real cheats)"
@command("test.protection_level_3", protection_level=3)
def x():
    return "you have acess to commands with protection level 3 (heavy cheats)"
@command("test.tree_say")
def c(text):
    '''[text:int] #arg obrigatório'''
    text = text
    return text

@command("test.kwargs")
def d(**kwags):
    '''{**kwargs_name} = #kwargs'''
    text = kwags["text"]
    return text

@command("test.args")
def e(*args):
    '''[*args_name] args'''
    text = ""
    for arg in args:
        text += f"{arg} "
    return text

@command("test.kwarg")
def d(kwarg="aaa"):
    '''{text:str} = " hello, world " kwarg n obrigatório'''
    text = kwarg
    return text



