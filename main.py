import sys
from get_user_input import display_help
from CommandParser import CommandParser
from FlashMessage import FlashMessage
# show tables
from src.database_show_tables import get_tables

# insert data 
from src.insert_table_data import insert_data

# desc table
from src.show_table_view import get_table_view

# show create table 
from src.show_table_structure import get_table_structure

# select * from table
from src.fetch_star_all import fetch_all

# this is the custom parser like active:: 
from src.custom_fetch_all import all

# insert data with foreign key, like table_name::withkey(['user_id' => 1]).single()
from _keys._foreing.foreign_key_data_insertion import insert_data_with_foreign_keys

# handle foreig keys, set 0 || 1 also, like active::foreign_key(0)
# enable::keys(details) || disable::keys(details)
from _keys._constraint.foreign_on_off import contstraint_handler

# use database_name, switch between databases or select database 
from src.use_database_selector import switch_database

#  initialize the database connection
from config.db_config import initialize
flash = FlashMessage()

query_running = False

def execute_command(
    command_input,
    db_list,
    table_list,
    column_information,
    fake_data,
    db_connection,
    current_db,
):
    global query_running  # Use the global variable to track query state
    """Execute a command based on user input."""
    parser = CommandParser(command_input)
    command = parser.get_command()

    if command == "show databases":
        db_list.get_database_list()
    elif command.startswith("use "):
        return switch_database(db_list, parser)
    elif command == "show tables":
        get_tables(current_db, table_list)
    elif command.startswith("table "):
        insert_data(
            command,
            parser,
            current_db,
            table_list,
            column_information,
            fake_data,
            db_connection,
        )
    elif command.startswith("desc "):
        get_table_view(command, parser, current_db, table_list)
    elif command.startswith("show create table"):
        get_table_structure(command, parser, current_db, table_list)
    elif command.startswith("select * from"):
        query_running = True  # Set flag to indicate query is running
        try:
            fetch_all(command, parser, current_db, table_list)
        except Exception as e:
            flash.error_message(f"An error occurred: {e}")
        finally:
            query_running = False
    elif "::withkey(" in command and (
        ").length(" in command or ").single()" in command
    ):
        insert_data_with_foreign_keys(
            command,
            current_db,
            table_list,
            column_information,
            fake_data,
            db_connection,
        )
    elif command.startswith("active::"):
        return contstraint_handler(command, current_db, db_connection)
    elif command.startswith("enable::") or command.startswith("disable::"):
        return contstraint_handler(command, current_db, db_connection)
    elif "::" in command:
        all(command, table_list)  # fetch all data post::all() || post::all(10)
    elif command in ["--help", "--h"]:
        display_help()
    elif command == "exit":
        flash.success_message("Exit command executed. Application terminating.")
        return "exit"
    else:
        flash.error_message(
            f"Invalid command: {command}. Type '--help' for a list of commands.",
            f"Invalid command entered: {command}",
        )
    return current_db


def is_running():
    global query_running
    try:
        
        db_connection, db_list, table_list, column_information, fake_data = initialize() # initizlize the database connection config/db_config
        
        print(
            "Welcome to the 'FastInsert' Type '--help' or '--h' for help. Type 'exit' to exit"
        )
        current_db = None
        # username = getpass.getuser()  # Get the username
        username = db_connection["username"]
        while True:
            try:
                prompt = (
                    f"{username.capitalize()}: FastInsert [{current_db}]> "
                    if current_db
                    else f"{username.capitalize()}: FastInsert> "
                )
                command_input = input(prompt).strip()
                current_db = execute_command(
                    command_input,
                    db_list,
                    table_list,
                    column_information,
                    fake_data,
                    db_connection,
                    current_db,
                )
                if current_db == "exit":
                    break
            except KeyboardInterrupt:
                if query_running:  # Check if a query is running
                    print("\nQuery cancelled. Continuing normally.")
                    query_running = False
                else:
                    print("\nPress Ctrl+C again to exit.")
                    while True:
                        try:
                            input(
                                "Press Ctrl+C again to exit, or press Enter to continue..."
                            )
                            break
                        except KeyboardInterrupt:
                            print("\nExiting program.")
                            db_connection["cnx"].close()
                            sys.exit(1)
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print("\nExiting program.")
            db_connection["cnx"].close()
            # sys.exit(1)
        else:
            print(f"An error occurred: {e}")
    finally:
        # db_connection["cnx"].close()
        sys.exit(0)


def main():
    is_running()


if __name__ == "__main__":
    main()
