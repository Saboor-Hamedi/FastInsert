import sys
import argparse
import mysql.connector
from typing import Dict, Tuple
from Style import  Style
from reports import  success_report, terminated_app
from input_utils import prompt_for_input, validate_port
from DatabaseConnection import DatabaseConnection
from FakerDataGenerator import FakerDataGenerator
from DatabaseManager import DatabaseManager
from TableManager import TableManager
from ColumnManager import ColumnManager
def get_args():
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
    
    collation = args.collation
    if not collation:
        collation = 'utf8mb4_unicode_ci' # default collation, but user can change it on login --collation 'your collation here'
    else: 
        collation = args.collation
    
        
    """Use the collected values to initialize the DatabaseConnection"""
    return host, user, password, port, collation


def create_database_connection(host:str, user:str, password:str, port:int, collation:str):
    try:
        return DatabaseConnection(
            host=host, user=user, password=password, port=port, collation=collation
        )
    except Exception as e:
        print(f"{Style.RED}Failed to create database connection: {e}{Style.RESET}")
        terminated_app('Failed to establish connection')
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
            terminated_app("Failed to initialize the database connection.")
            sys.exit(1)
        return cnx
    except ConnectionError as e:
        print(f"{Style.RED}{e}{Style.RESET}")
        terminated_app(f"Connection error: {e}")
        sys.exit(1)
        
def connect_to_database() -> Dict:
    """Establish a database connection and return a dictionary with the connection and cursor."""
    cnx = initialize_database_connection()
    cursor = cnx.cursor
    return {"cnx": cnx, "cursor": cursor} 

def create_managers(db_connection:Dict)->Tuple:
    """Create database manager"""
    try:
        success_report('Starting main function')
        db_list = DatabaseManager(db_connection['cursor'])
        table_list = TableManager(db_connection['cursor'])
        column_information = ColumnManager(db_connection['cursor'])
        fake_data = FakerDataGenerator(db_connection['cnx'])
        return db_list, table_list, column_information, fake_data
    except mysql.connector as err:
        terminated_app(f'Check your database db_connection: {err}')
        print(f'Cannot create database manager: {err}')
        return()
    
def display_help():
    success_report("Help command executed.")
    print("Available commands:")
    print("  SHOW DATABASES - List all databases")
    print("  USE <database_name> - Select a database")
    print("  SHOW TABLES - List all tables in the selected database")
    print("  SELECT TABLE <table_name> - Select a table to insert data")
    print("  SELECT * TABLE <table_name->all()> - Display all data")
    print("  EXIT - Exit the program")