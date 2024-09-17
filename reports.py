
import logging


logging.basicConfig(filename='db_explorer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def success_report():
    return logging.info("Starting the application")

def terminated_app():
    logging.info("Application terminated successfully")