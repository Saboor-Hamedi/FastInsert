import sys



# class Style():
#     BLACK = '\033[30m'
#     RED = '\033[31m'
#     GREEN = '\033[32m'
#     YELLOW = '\033[33m'
#     BLUE = '\033[34m'
#     MAGENTA = '\033[35m'
#     CYAN = '\033[36m'
#     WHITE = '\033[37m'
#     UNDERLINE = '\033[4m'
#     RESET = '\033[0m'
class Style():
    def __init__(self):
        self.is_terminal = self._is_terminal()

    def _is_terminal(self):
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    @property
    def BLACK(self):
        return '\033[30m' if self.is_terminal else ''

    @property
    def RED(self):
        return '\033[31m' if self.is_terminal else ''

    @property
    def GREEN(self):
        return '\033[32m' if self.is_terminal else ''

    @property
    def YELLOW(self):
        return '\033[33m' if self.is_terminal else ''

    @property
    def BLUE(self):
        return '\033[34m' if self.is_terminal else ''

    @property
    def MAGENTA(self):
        return '\033[35m' if self.is_terminal else ''

    @property
    def CYAN(self):
        return '\033[36m' if self.is_terminal else ''

    @property
    def WHITE(self):
        return '\033[37m' if self.is_terminal else ''

    @property
    def UNDERLINE(self):
        return '\033[4m' if self.is_terminal else ''

    @property
    def RESET(self):
        return '\033[0m' if self.is_terminal else ''