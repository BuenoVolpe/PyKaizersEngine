from engine.configs.configs import configs
#=====================================#
from engine.console.utils import parse_args, parse_value, split_command
#=====================================#
from engine.utils.debug_log import log_error, log_success
#=====================================#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#=====================================#
class Console:
    def __init__(self):
        #-------------------------------------#
        self.visible = True
        #-------------------------------------#
        self.commands = {}
        #-------------------------------------#
        self.protection_level = configs.console.level
        signal_bus.subscribe(signals.EXECUTE_COMMAND, self.execute_command, priority=signals_prioritys.PRE_LAST)
        #-------------------------------------#
    #=====================================#
    def execute_command(self, string:str):
        #-------------------------------------#
        cmd_name, args_text = split_command(string)
        #-------------------------------------#
        if cmd_name not in self.commands:
            log_error(f"[console]: command '{cmd_name}' is unknown")
            return
        #-------------------------------------#
        cmd = self.commands[cmd_name]
        #-------------------------------------#
        args, kwargs = parse_args(args_text)
        #-------------------------------------#
        result = cmd["func"](*args, **kwargs)
        #-------------------------------------#
        if result is not None:
            log_success(result)
    #=====================================#
    def register(self, name:str, func, protection_level:int=1):
        #--------------------------------#
        node = self.commands
        key = name.replace(".", " ")
        #--------------------------------#
        node[key] = {
            "func": func,
            "help": func.__doc__ or "No description",
            "protection":protection_level
        }
#================================#
console = Console()
#================================#
def command(name, protection_level:int=1, groups=[]):
    """protection level 0 -> 3
        0:not cheats
        1:simple cheats
        2:more heavy cheats, can cause some problens 
        3:commands that could broke the game
    """
    #--------------------------------#
    def wrapper(func):
        #--------------------------------#
        for group in groups:
            #--------------------------------#
            if group == "None":
                #--------------------------------#
                console.register(f"{name}", func, protection_level)
                continue
            #--------------------------------#
            console.register(f"{group}.{name}", func, protection_level)
        #--------------------------------#
        console.register(name, func, protection_level)
        return func
    #--------------------------------#
    return wrapper

