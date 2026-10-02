#============================================================#
import inspect
import __main__
from pathlib import Path
#============================================================#
main_file = Path(inspect.getsourcefile(__main__)).resolve()
project_root = main_file.parent
#============================================================#
def _get_namespace(file):
    #------------------------------------------------------------#
    file = Path(file).resolve()
    #------------------------------------------------------------#
    try:
        relative = file.relative_to(project_root)
    except ValueError:
        return None
    #------------------------------------------------------------#
    if not relative.parts:
        return None
    #------------------------------------------------------------#
    root = relative.parts[0]
    return root
    #------------------------------------------------------------#
#============================================================#
def _build_origin(callback):
    #------------------------------------------------------------#
    try:
        #------------------------------------------------------------#
        file = inspect.getsourcefile(callback)
        line = inspect.getsourcelines(callback)[1]
        #------------------------------------------------------------#
        qualname = getattr(
            callback,
            "__qualname__",
            callback.__name__
        )
        #------------------------------------------------------------#
        namespace = _get_namespace(file)
        #------------------------------------------------------------#
        return {
            'qualname':qualname,
            'namespace':namespace,
            'file':file,
            'line':line,
        }
    #------------------------------------------------------------#
    except Exception:
        return repr(callback)