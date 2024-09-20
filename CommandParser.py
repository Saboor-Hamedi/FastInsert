class CommandParser:
    """
    A class to parse and extract information from user input commands.

    This class takes a command string as input, strips and lowers the case, and splits it into individual words.
    It provides methods to get the entire command, get a specific argument, and get the remaining arguments starting from a specific index.

    Attributes:
        command (list): A list of words in the command string.

    Methods:
        get_command(): Returns the entire command as a string.
        get_arg(index=1, default=None): Returns the argument at a specific index, or a default value if the index is out of range.
        get_remaining_args(start=1): Returns the remaining arguments starting from a specific index.
    """
    def __init__(self, command):
        self.command = command.strip().lower().split()
        
    def get_command(self):
        #  Get the entire command
        return ' '.join(self.command)
    def get_arg(self, index =1 , default = None):
        # Get the argument at specific  index
        return self.command[index] if len(self.command) > index else default
    def get_remaining_args(self, start=1):
        """Get the remaining arguments starting from a specific index."""
        
        return self.command[start:]