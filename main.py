import sys
import re
from get_user_input import connect_to_database, create_managers, display_help
from CommandParser import CommandParser
from FlashMessage import FlashMessage
from ForeignKeyInserter import ForeignKeyInserter
from HandleKeys import HandleKeys

# show tables
from src.database_show_tables import get_tables

# insert data 
from src.insert_table_data import insert_data

# desc table
from src.show_table_view import get_table_view

# show create table 
from src.show_table_structure import get_table_structure

# select * from table
from src.fetch_stars_all_data import fetch_all
flash = FlashMessage()


def handle_us_db(db_list, parser):
    """Select a database based on user input."""
    db_name = parser.get_arg()
    if db_list.check_database(db_name):
        db_list.select_database(db_name)
        return db_name
    else:
        flash.error_message(
            f"ERROR 1049 (42000): Unknown database '{db_name}' ",
            f"{db_name} does not exist",
        )

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
        return handle_us_db(db_list, parser)
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
        handle_insert_with_key(
            command,
            current_db,
            table_list,
            column_information,
            fake_data,
            db_connection,
        )
    elif command.startswith("active::"):
        return handle_keys(command, current_db, db_connection)
    elif command.startswith("enable::") or command.startswith("disable::"):
        return handle_keys(command, current_db, db_connection)
    elif "::" in command:
        handle_custom_syntax(command, table_list)
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

def handle_custom_syntax(command, table_list):
    """Handle custom syntax like 'table::all()' or 'table::all(<limit>)'."""
    parts = command.split("::")
    if len(parts) == 2:
        table_name = parts[0].strip()
        action_part = parts[1].strip()
        if action_part == "all" or (
            action_part.startswith("all(") and action_part.endswith(")")
        ):
            limit = None
            if "(" in action_part and action_part.endswith(")"):
                limit_str = action_part[
                    action_part.index("(") + 1 : action_part.index(")")
                ].strip()
                if limit_str.isdigit():
                    limit = int(limit_str)
                elif limit_str:
                    print(f"Invalid limit value: {limit_str}. Please enter an integer.")
                    return
            table_list.all(table_name, limit)
        else:
            flash.error_message(
                f"Invalid action: {action_part}. Use 'table::all()' or 'table::all(<limit>)'."
            )
    else:
        flash.error_message(
            f"Invalid command: {command}. Type '--help' for a list of commands."
        )


def handle_insert_with_key(
    command, current_db, table_list, column_information, fake_data, db_connection
):
    """Handle the custom insert command with foreign keys."""
    if not current_db:
        flash.error_message(
            "No database selected. Use the 'use <database_name>' command first.",
            "No database selected.",
        )
        return
    try:
        table_name = command.split("::")[0]
        # Parse withkey part
        key_part_match = re.search(r"::withkey\(\[(.*?)\]\)", command)
        if not key_part_match:
            flash.error_message("Invalid syntax for withkey part.")
            return
        key_part = key_part_match.group(1)
        key_dict = {}
        for pair in key_part.split(","):
            key, value = pair.strip().split("=>")
            key_dict[key.strip().strip("'").strip('"')] = int(value.strip())

        # Check for .single() or .length(n) part
        length_match = re.search(r"\.length\((\d+)\)", command)
        single_match = re.search(r"\.single\(\)", command)
        if length_match:
            num_records = int(length_match.group(1))
        elif single_match:
            num_records = 1
        else:
            flash.error_message("Invalid syntax for length or single part.")
            return
        # tables = [table.lower() for table in table_list.show_tables(current_db)]
        if table_name:
            foreignKey = ForeignKeyInserter(db_connection, table_name, key_dict)
            columns = column_information.get_column_information(current_db, table_name)
            foreignKey.insert_data_with_keys(
                db_connection["cnx"],
                db_connection["cursor"],
                current_db,
                table_name,
                num_records,
                columns,
                key_dict,
            )
        else:
            flash.error_message(
                f"Table {table_name} does not exist in database {current_db}."
            )
    except Exception as e:
        flash.error_message(f"An error occurred: {e}")


def handle_keys(command, current_db, db_connection):
    if not current_db:
        flash.error_message(
            "No database selected. Use the 'use <database_name>' command first.",
            "No database selected.",
        )
        return
    try:
        handl_keys = HandleKeys(db_connection)
        if command == "active::foreign_key(0)":
            handl_keys.disable_foreign_keys()  # Disable foreign key checks in DB
            flash.success_message("Foreign key checks disabled.")
        elif command == "active::foreign_key(1)":
            handl_keys.enable_foreign_keys()  # Enable foreign key checks in DB
            flash.success_message("Foreign key checks enabled.")
        elif command.startswith("enable::keys("):
            table_name = command.split("enable::keys(")[-1].strip(")")
            handl_keys.enable_keys(table_name)
            flash.success_message(
                f"Keys enabled for table {table_name}.",
                f"Keys enabled for table {table_name}.",
            )
        elif command.startswith("disable::keys("):
            table_name = command.split("disable::keys(")[-1].strip(")")
            handl_keys.disable_keys(table_name)
            flash.success_message(
                f"Keys disabled for table {table_name}.",
                f"Keys disabled for table {table_name}.",
            )
        else:
            flash.error_message(
                "Invalid syntax. Use 'active::foreign_key(0)' or 'active::foreign_key(1)'"
            )
        return current_db
    except Exception as err:
        flash.error_message(f"Something went wrong with the key {err}")



def is_running():
    global query_running
    try:
        """Main function and database handling."""
        db_connection = connect_to_database()
        db_list, table_list, column_information, fake_data = create_managers(
            db_connection
        )
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
