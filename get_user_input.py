from input_utils import prompt_for_input, validate_port
from DatabaseConnection import DatabaseConnection
import argparse
from reports import success_report, terminated_app
from input_utils import prompt_for_input, validate_port
import sys
from Style import Style


def get_user_input()-> str:
    print("\nSelect an option:")
    print("[1] List databases")
    print("[2] Select database")
    print("[0] Exit")
    return input("Enter your choice: ")


def get_args():
    success_report()
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Database Explorer")
    parser.add_argument("--host", help="Database host")
    parser.add_argument("--user", help="Database user")
    parser.add_argument("--password", help="Database password")
    parser.add_argument("--port", type=int, help="Database port")
    parser.add_argument("--collation", help="Database collation")
    return parser.parse_args()  # Parse command-line arguments


def prompt_for_database_details(args):
    # Prompt the user for missing arguments
    host = args.host or prompt_for_input("Enter database host: ", "localhost")
    user = args.user or prompt_for_input("Enter database user: ", "root")
    password = args.password or prompt_for_input(
        "Enter database password: ", "", hide_input=True
    )
    port = args.port or int(
        prompt_for_input("Enter database port: ", 3306, validate=validate_port)
    )
    collation = args.collation or prompt_for_input(
        "Enter database collation: ", "utf8mb4_unicode_ci"
    )
    """Use the collected values to initialize the DatabaseConnection"""
    return host, user, password, port, collation


def create_database_connection(host:str, user:str, password:str, port:int, collation:str):
    try:
        return DatabaseConnection(
            host=host, user=user, password=password, port=port, collation=collation
        )
    except Exception as e:
        print(f"{Style.RED}Failed to create database connection: {e}{Style.RESET}")
        terminated_app()
        sys.exit(1)
    


def initialize_database_connection() -> DatabaseConnection:
    try:
        args = get_args()
        host, user, password, port, collation = prompt_for_database_details(args)
        cnx = create_database_connection(host, user, password, port, collation)
        if not cnx.connect():
            print(
                f"{Style.RED}Failed to initialize the database connection.{Style.RESET}"
            )
            terminated_app()
            sys.exit(1)
        terminated_app()
        return cnx
    except ConnectionError as e:
        print(f"{Style.RED}{e}{Style.RESET}")
        terminated_app()
        sys.exit(1)
