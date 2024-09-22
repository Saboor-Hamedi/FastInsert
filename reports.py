import logging

logging.basicConfig(filename='db_explorer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_success(message="Operation completed successfully"):
    logging.info(message)


def log_error(message="Application terminated"):
    logging.error(message)
