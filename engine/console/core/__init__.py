import pygame as pg
import inspect
import shlex
#--------------------------------#
from engine.console.core.log import ConsoleLog
from engine.console.core.executer import ConsoleExecute
#--------------------------------#
from engine.handlers.text_input import TextInput
from engine.configs.settings import settings
from engine.utils.scaler import scaler
#================================#
class ConsoleCore:
    def __init__(self, parent):
        #--------------------------------#
        self.show_signature = True
        #--------------------------------#
        self.parent = parent
        self.log = parent
        self.text_input = TextInput()
        self.console_log = ConsoleLog(self, parent)
        self.executer = ConsoleExecute(self, parent)
        #--------------------------------#
        self.autocomplete_candidates = []
        self.autocomplete_index = 0
        #--------------------------------#
        self.history = []
        self.max_lines = settings.get("console_max_lines", 100)
        self.scroll_y = 0
    #================================#
    def navigate_command(self, parts):
        #--------------------------------#
        node = self.parent.commands
        #--------------------------------#
        last_valid_node = None
        consumed = 0
        #--------------------------------#
        for i, part in enumerate(parts):
            #--------------------------------#
            if not isinstance(node, dict):
                break
            #--------------------------------#
            if part not in node:
                break
            #--------------------------------#
            node = node[part]
            #--------------------------------#
            if isinstance(node, dict) and "func" in node:
                #--------------------------------#
                last_valid_node = node
                consumed = i + 1
        #--------------------------------#
        return last_valid_node, consumed, node
    #================================#
    def get_suggestions(self, text: str):
        #--------------------------------#
        try:
            parts = shlex.split(text, posix=False)
        except:
            parts = text.split()
        #--------------------------------#
        if text.endswith(" "):
            parts.append("")
        #--------------------------------#
        if not parts:
            parts = [""]
        #--------------------------------#
        node = self.parent.commands
        #================================#
        #navigates the most possible
        consumed = 0
        #--------------------------------#
        for i, part in enumerate(parts):
            #--------------------------------#
            if not isinstance(node, dict):
                break
            #--------------------------------#
            if part not in node:
                break
            #--------------------------------#
            node = node[part]
            consumed = i + 1
        #--------------------------------#
        suggestions = []
        #================================#
        #if still instill in comands/subcomands
        current = parts[-1] if parts else ""
        #--------------------------------#
        if isinstance(node, dict):
            #--------------------------------#
            for key in sorted(node.keys()):
                #--------------------------------#
                if key in ["func", "help", "protection"]:
                    continue
                #--------------------------------#
                if key.startswith(current):
                    #--------------------------------#
                    value = node[key]
                    #--------------------------------#
                    display = key
                    #--------------------------------#
                    if isinstance(value, dict) and "func" in value:
                        #--------------------------------#
                        signature = get_command_signature(value["func"])
                        if signature:
                            display += " " + signature
                    #--------------------------------#
                    suggestions.append({
                        "replace": key,
                        "display": display
                    })
            #--------------------------------#
            return suggestions
        #================================#
        #signature
        if isinstance(node, dict) and "func" in node:
            #--------------------------------#
            signature = get_command_signature(node["func"])
            #--------------------------------#
            if signature:
                self.show_signature = True
                suggestions.append({
                    "replace": "",
                    "display": signature
                })

        return suggestions

    #================================#
    def events(self, event):
        if self.parent.visible:
            #--------------------------------#
            result = self.text_input.handle_event(event)
            #--------------------------------#
            if event.type == pg.KEYDOWN:
                #--------------------------------#
                if event.key not in [pg.K_RETURN, pg.K_TAB]:
                    self.reset_autocomplete_candidates()
                #--------------------------------#
                if event.key == pg.K_PAGEUP:
                    self.scroll_y = max(0, self.scroll_y + 1)
                elif event.key == pg.K_PAGEDOWN:
                    self.scroll_y = min(self.scroll_y - 1, self.max_scroll())
            #--------------------------------#
            if result is not None:
                if result == "__TAB__":
                    #--------------------------------#
                    if self.autocomplete_candidates:
                        #--------------------------------#
                        self.autocomplete_index += 1
                        self.autocomplete_index %= min(settings.get("console_max_autocomplete_candidates", 4), len(self.autocomplete_candidates))
                        suggestion = self.autocomplete_candidates[
                            self.autocomplete_index
                        ]["replace"]
                        #--------------------------------#
                        parts = shlex.split(self.text_input.text)
                        #--------------------------------#
                        if self.text_input.text.endswith(" "):
                            parts.append("")
                        #--------------------------------#
                        if parts:
                            parts[-1] = suggestion
                        else:
                            parts = [suggestion]
                        #--------------------------------#
                        self.text_input.set_text(" ".join(parts))
                        #--------------------------------#
                        # self.reset_autocomplete_candidates()
                    #--------------------------------#
                    return
                if result == "__BACKSPACE__":
                    self.reset_autocomplete_candidates()
                    return
                #--------------------------------#
                self.reset_autocomplete_candidates()
                #--------------------------------#
                text = result
                #--------------------------------#
                self.console_log.command_log(text)
                success = self.executer.execute(text)
                #--------------------------------#
                # if success and text not in self.command_history:
                #     self.command_history.append(text)
                #     self.history_index = len(self.command_history)
    #================================#
    def reset_autocomplete_candidates(self):
        #--------------------------------#
        self.autocomplete_candidates = self.get_suggestions(
            self.text_input.text
        )
        #--------------------------------#
        self.autocomplete_index = 0
    #================================#
    def max_scroll(self):
        return max(0, len(self.history) - self.parent.ui.visible_lines)
    #================================#


def get_command_signature(func):
    sig = inspect.signature(func)
    #--------------------------------#
    result = []
    #--------------------------------#
    for name, param in sig.parameters.items():
        #--------------------------------#
        if param.default == inspect.Parameter.empty:
            result.append(f"[{name}]")
        else:
            result.append(f"{{{name}={param.default}}}")
    #--------------------------------#
    return " ".join(result)

