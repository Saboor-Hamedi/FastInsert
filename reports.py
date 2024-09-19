import logging

logging.basicConfig(filename='db_explorer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def success_report(message="Operation completed successfully"):
    logging.info(message)


def terminated_app(message="Application terminated"):
    logging.error(message)
