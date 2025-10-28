from datetime import datetime
import os

# ANSI colors
_COLORS = {
    "info": "\033[34m",     # blue
    "debug": "\033[90m",    # gray
    "warning": "\033[33m",  # yellow
    "error": "\033[31m",    # red
}
_RESET = "\033[0m"


def _strip_ansi(s: str) -> str:
    for c in _COLORS.values():
        s = s.replace(c, "")
    return s.replace(_RESET, "")


def smart_log(*args, **kwargs) -> None:
    
    level = str(kwargs.get("level", "info")).lower()
    timestamp = bool(kwargs.get("timestamp", True))
    show_date = bool(kwargs.get("date", False))
    colored = bool(kwargs.get("colored", kwargs.get("color", True)))
    save_path = kwargs.get("save_to_file", kwargs.get("save_to", None))

    prefix = ""
    if timestamp or show_date:
        now = datetime.now()
        parts = []
        if show_date:
            parts.append(now.strftime("%Y-%m-%d"))
        if timestamp:
            parts.append(now.strftime("%H:%M:%S"))
        prefix = " ".join(parts) + " "

    msg = " ".join(map(str, args))
    tag = f"[{level.upper()}]"
    line = f"{prefix}{tag} {msg}"

    if colored and level in _COLORS:
        display = f"{_COLORS[level]}{line}{_RESET}"
    else:
        display = line

    print(display)

    if save_path:
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(save_path, "a", encoding="utf-8") as f:
            f.write(_strip_ansi(line) + "\n")
