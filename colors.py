try:
    import colorama
    colorama.init()
except ImportError:
    pass

class FGColors:
    def __init__(self):
        self.black = "\x1b[30m"
        self.red = "\x1b[31m"
        self.green = "\x1b[32m"
        self.yellow = "\x1b[33m"
        self.blue = "\x1b[34m"
        self.magenta = "\x1b[35m"
        self.cyan = "\x1b[36m"
        self.white = "\x1b[37m"
        self.gray = "\x1b[90m"
        self.crimson = "\x1b[38m"

class BGColors:
    def __init__(self):
        self.black = "\x1b[40m"
        self.red = "\x1b[41m"
        self.green = "\x1b[42m"
        self.yellow = "\x1b[43m"
        self.blue = "\x1b[44m"
        self.magenta = "\x1b[45m"
        self.cyan = "\x1b[46m"
        self.white = "\x1b[47m"
        self.gray = "\x1b[100m"
        self.crimson = "\x1b[48m"

class Colours:
    def __init__(self):
        self.reset = "\x1b[0m"
        self.bright = "\x1b[1m"
        self.dim = "\x1b[2m"
        self.underscore = "\x1b[4m"
        self.blink = "\x1b[5m"
        self.reverse = "\x1b[7m"
        self.hidden = "\x1b[8m"
        self.fg = FGColors()
        self.bg = BGColors()

def lookup_fg(colours, key):
    fg_colors = {
        "black": colours.fg.black,
        "red": colours.fg.red,
        "green": colours.fg.green,
        "yellow": colours.fg.yellow,
        "blue": colours.fg.blue,
        "magenta": colours.fg.magenta,
        "cyan": colours.fg.cyan,
        "white": colours.fg.white,
        "gray": colours.fg.gray,
        "crimson": colours.fg.crimson
    }
    return fg_colors.get(key, colours.fg.red)