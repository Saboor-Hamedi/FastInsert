class CommandParser:
    
    def __init__(self, command):
        """
        Initialize the CommandParser object.

        Args:
            command (str): The command string to be parsed.

        Returns:
            None
        """
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
    
    def split(self, separator):

        return self.get_command().split(separator)
    
    