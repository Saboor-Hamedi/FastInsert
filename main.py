
from typing import Dict
from FakerDataGenerator import FakerDataGenerator
from DatabaseManager import DatabaseManager
from ListTable import ListTable
from ColumnManager import ColumnManager
from Style import Style
from get_user_input import initialize_database_connection
from reports import success_report, terminated_app


def connect_to_database() -> Dict:
    """Establish a database connection and return a dictionary with the connection and cursor."""
    cnx = initialize_database_connection()
    cursor = cnx.cursor
    return {"cnx": cnx, "cursor": cursor}


def main():
    """Main function and database handling"""
    success_report('Starting main function')
    db_connection = connect_to_database()
    db_list = DatabaseManager(db_connection["cursor"])
    table_list = ListTable(db_connection["cursor"])
    column_information = ColumnManager(db_connection["cursor"])
    fake_data = FakerDataGenerator(db_connection["cnx"])

    print(
        f"Welcome to the {Style.BLUE} 'FastInsert' {Style.RESET} Type '--help' or '--h' for help. Type 'exit' to exit"
    )

    current_db = None

    while True:
        if current_db:
            prompt = f"FastInsert [{current_db}]> "
        else:
            prompt = "FastInsert> "
        command = input(prompt).strip().lower()

        if command == "show databases":
            db_list.get_database_list()
        elif command.startswith("use "):
            db_name = command.split(" ", 1)[1]
            if db_list.check_database(db_name):
                current_db = db_name
                db_list.select_database(db_name)
                # success_report(f'Database change to {db_name}')
            else:
                print(f"Database {db_name} does not exist.")
                terminated_app(f'Attemp to use that database {db_name} does not exists')
        elif command == "show tables":
            if current_db:
                table_list.list_tables(current_db)
            else:
                print("No database selected. Use the 'use <database_name>' command first.")
                terminated_app('No database selected when attempting to show tables')
        elif command.startswith("table "):
            if current_db:
                table_name = command.split(" ", 1)[1]
                tables = [table.lower() for table in table_list.list_tables(current_db)]
                if table_name in tables:
                    columns = column_information.get_column_information(current_db, table_name)
                    print(f"columns in {table_name}")
                    for col in columns:
                        print(f" - {col[0]} ({col[1]})")
                    try:
                        num_records = int(input("Enter the number of records to insert: "))
                        fake_data.insert_data(
                            db_connection["cnx"],
                            db_connection["cursor"],
                            current_db,
                            table_name,
                            num_records,
                            columns,
                        )
                        success_report(f'Inserted {num_records} records into {table_name}')
                    except ValueError:
                        print("Invalid number of records. Please enter an integer.")
                        terminated_app("Invalid number of records entered.")
                else:
                    print(f"Table {table_name} does not exist in database {current_db}.")
                    terminated_app(f"Attempted to select a non-existent table: {table_name}")
            else:
                print("No database selected. Use the 'use <database_name>' command first.")
                terminated_app("No database selected when attempting to select a table.")
        elif command == "--help" or command == "--h":
            success_report("Help command executed.")
            print("Available commands:")
            print("  SHOW DATABASES - List all databases")
            print("  USE <database_name> - Select a database")
            print("  SHOW TABLES - List all tables in the selected database")
            print("  SELECT TABLE <table_name> - Select a table to insert data")
            print("  EXIT - Exit the program")
        elif command == "exit":
            success_report("Exit command executed. Application terminating.")
            break
        else:
            print(f"Invalid command: {command}. Type '--help' for a list of commands.")
            terminated_app(f"Invalid command entered: {command}")


if __name__ == "__main__":
    main()
