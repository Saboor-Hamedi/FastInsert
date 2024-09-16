import maskpass

from Style import Style

def prompt_for_input(prompt, default=None, hide_input=False, validate=None):
    while True:
        if hide_input:
            user_input = maskpass.askpass(f"{prompt} (default '{default}'): ")
        else:
            user_input = input(f"{prompt} (default '{default}'): ")

        if not user_input:
            user_input = default

        if validate:
            try:
                validate(user_input)
                return user_input
            except ValueError as e:
                print(e)
        else:
            return user_input

# def validate_port(port):
#     if not (1 <= port <= 65535):
#         raise ValueError(f"{Style.BLUE}Port number must be between 1 and {Style.RED}{port}. {Style.RESET}")

def validate_port(port_str):
    try:
        port = int(port_str)
        if not (1 <= port <= 65535):
            raise ValueError(f"{Style.BLUE}Port number must be between 1 and {Style.RED}{port}. {Style.RESET}")
    except ValueError:
        raise ValueError(f"{Style.BLUE}Invalid port number. It must be an integer between 1 and {Style.RED}{port}. {Style.RESET}.")
