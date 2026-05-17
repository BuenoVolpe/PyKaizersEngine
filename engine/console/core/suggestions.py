import shlex
import inspect

class ConsoleSuggestions:
    def __init__(self, core, parent):
        self.core = core
        self.parent = parent

        self.candidates = []
        self.index = 0
        self.show_signature = True

    #================================#
    def reset(self):
        self.candidates = self.build(self.core.text_input.text)
        self.index = 0

    #================================#
    def build(self, text: str):
        try:
            parts = shlex.split(text, posix=False)
        except:
            parts = text.split()

        if text.endswith(" "):
            parts.append("")

        if not parts:
            parts = [""]

        node = self.parent.commands

        for part in parts:
            if not isinstance(node, dict):
                break
            if part not in node:
                break
            node = node[part]

        current = parts[-1] if parts else ""
        suggestions = []

        # =====================================
        if isinstance(node, dict):
            for key in sorted(node.keys()):
                if key in ["func", "help", "protection"]:
                    continue

                if key.startswith(current):
                    value = node[key]
                    display = key

                    if isinstance(value, dict) and "func" in value:
                        sig = get_command_signature(value["func"])
                        if sig:
                            display += " " + sig

                    suggestions.append({
                        "replace": key,
                        "display": display
                    })

            return suggestions

        # =====================================
        if isinstance(node, dict) and "func" in node:
            sig = get_command_signature(node["func"])
            if sig:
                suggestions.append({
                    "replace": "",
                    "display": sig
                })

        return suggestions

    #================================#
    def next(self):
        if not self.candidates:
            return None

        self.index = (self.index + 1) % min(
            4,
            len(self.candidates)
        )

        return self.candidates[self.index]["replace"]
    #================================#
    def current(self):
        if not self.candidates:
            return None
        return self.candidates[self.index]


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

