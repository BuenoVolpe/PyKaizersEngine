from engine.console import command, console
from engine.configs.settings import settings
#--------------------------------#
from engine.utils.log import log, log_success, log_error
from engine.console.ui.surface import ConsoleSurface
#================================#
@command("console.settings.set", protection_level=1)
def settings_set(key, value):
    #--------------------------------#
    settings.set(key, value)
#================================#
@command("console.settings.get", protection_level=1)
def settings_get(key):
    #--------------------------------#
    value = settings.get(key)
    if value is None:
        log_error(f"settings has no key: {key}")
        return
    #--------------------------------#
    return f"{key}: {value}"
    

