import logging
import re

def remove_ansi_codes(message):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', message)

def fix_ansi_logging(func):
    def wrapper(message, *args, **kwargs):
        clean_message = remove_ansi_codes(message)
        return func(clean_message, *args, **kwargs)
    return wrapper

logging.info = fix_ansi_logging(logging.info)
logging.error = fix_ansi_logging(logging.error)
logging.basicConfig(filename='db_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_success(message="Operation completed successfully"):
    logging.info(message)

def log_error(message="Application terminated"):
    logging.error(message)
