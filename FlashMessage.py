from loggin import log_error, log_success
from Style import Style

class FlashMessage:
    def error_message(self, message: str, db_logs: str = '') -> None:
        """Prints an error message and logs it."""
        print(f"{Style().RED}Error: {message}{Style().RESET}")
        log_error(db_logs if db_logs else message)

    def success_message(self, message: str, db_logs: str = '') -> None:
        """Prints a success message and logs it."""
        print(f"{Style().GREEN}Success: {message} {Style().RESET}")
        log_success(db_logs if db_logs else message)