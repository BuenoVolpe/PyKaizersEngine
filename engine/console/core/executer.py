import pygame as pg
#--------------------------------#
import shlex
import inspect
#--------------------------------#
from engine.handlers.text_input import TextInput
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class ConsoleExecute:
    def __init__(self, parent, grandparent):
        #--------------------------------#
        self.grandparent = grandparent
        self.parent = parent
        #--------------------------------#
        self.log = self.parent.console_log.log
        self.error = self.parent.console_log.error
        self.success = self.parent.console_log.success
        self.command = self.parent.console_log.command_log
    #================================#
    def execute(self, raw:str):
        #--------------------------------#
        try:
            parts = shlex.split(raw.strip())
        except ValueError as e:
            self.error(f"Syntax error: {e}")
            return False
        #--------------------------------#
        if not parts:
            return False
        #--------------------------------#
        func = None
        consumed = 0
        entry = {}
        game = self.grandparent.game
        #--------------------------------#
        func, entry, consumed = self.navigate_tree(parts)
        #--------------------------------#
        if not func:
            self.error("Unknown command")
            return False
        #--------------------------------#
        if entry.get("protection", self.grandparent.console_permition+1) > self.grandparent.console_permition:
            self.error(f"your permision {self.grandparent.console_permition} is below the command protection level {entry.get("protection")}")
            return False
        #--------------------------------#
        pos_args, kw_args = parse_args(parts[consumed:])
        #--------------------------------#
        try:
            #--------------------------------#
            result = func(*pos_args, **kw_args)
            #--------------------------------#
            if result is not None:
                #--------------------------------#
                self.success(result)
            #--------------------------------#
            return True
        #--------------------------------#
        except Exception as e:
            #--------------------------------#
            self.error(str(e))
            return False
    #================================#
    def navigate_tree(self, parts):
        node = self.grandparent.commands
        func = None
        consumed = 0
        entry = {}
        #--------------------------------#
        for i, part in enumerate(parts):
            #--------------------------------#
            if not isinstance(node, dict) or part not in node:
                break
            #--------------------------------#
            node = node[part]   
            #--------------------------------#
            if isinstance(node, dict) and "func" in node:
                #--------------------------------#
                func = node["func"]
                entry = node
                consumed = i + 1
                #--------------------------------#
                break
        #--------------------------------#
        return func, entry, consumed

#================================#
def parse_args(args):
    #--------------------------------#
    positional = []
    kwargs = {}
    #--------------------------------#
    for arg in args:
        #--------------------------------#
        if "=" in arg:
            #--------------------------------#
            key, value = arg.split("=", 1)
            kwargs[key] = auto_convert(value)
        #--------------------------------#
        else:
            positional.append(auto_convert(arg))
    #--------------------------------#
    return positional, kwargs
#================================#
import ast

#================================#
def auto_convert(value):
    #--------------------------------#
    if not isinstance(value, str):
        return value

    #--------------------------------#
    v = value.strip()

    #--------------------------------#
    low = v.lower()

    if low == "true":
        return True

    if low == "false":
        return False

    if low == "none":
        return None

    #--------------------------------#
    try:
        return ast.literal_eval(v)

    #--------------------------------#
    except (ValueError, SyntaxError):
        return v
    
