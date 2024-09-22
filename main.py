from Style import Style
import sys
import mysql.connector
from get_user_input import connect_to_database, create_managers, display_help
from reports import log_success, log_error
from CommandParser import CommandParser


def handle_us_db(db_list, parser):
    """Select a database based on user input."""
    db_name = parser.get_arg()
    if db_list.check_database(db_name):
        db_list.select_database(db_name)
        return db_name
    else:
        error_message = f"ERROR 1049 (42000): Unknown database '{db_name}'"
        print(error_message)
        log_error(error_message)


def handle_show_tables(current_db, table_list):
    try:
        if current_db:
            return table_list.show_tables(current_db)
        else:
            log_error("No database selected when attempting to show tables")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


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
        handle_show_tables(current_db, table_list)
    elif command.startswith("table "):
        handle_insert_data(
            command,
            parser,
            current_db,
            table_list,
            column_information,
            fake_data,
            db_connection,
        )
    elif command.startswith("desc "):
        handle_desc_table(command, parser, current_db, table_list)
    elif command.startswith("show create table"):
        handle_show_create_table(command, parser, current_db, table_list)
    elif command.startswith("select * from"):
        query_running = True  # Set flag to indicate query is running
        try:
            handle_select_all(command, parser, current_db, table_list)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            query_running = False
    elif "->" in command:
        handle_custom_syntax(command, table_list)
    elif command in ["--help", "--h"]:
        display_help()
    elif command == "exit":
        log_success("Exit command executed. Application terminating.")
        return "exit"
    else:
        print(f"Invalid command: {command}. Type '--help' for a list of commands.")
        log_error(f"Invalid command entered: {command}")
    return current_db


def handle_insert_data(
    command,
    parser,
    current_db,
    table_list,
    column_information,
    fake_data,
    db_connection,
):
    """Handle the 'table' command to insert data."""
    if current_db:
        # table_name = command.split(" ", 1)[1]
        table_name = parser.get_arg()
        tables = [table.lower() for table in table_list.show_tables(current_db)]
        if table_name in tables:
            columns = column_information.get_column_information(current_db, table_name)
            # print(f"columns in {table_name}") # show columns
            # for col in columns:
            #     print(f" - {col[0]} ({col[1]})")
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
                log_success(f"Inserted {num_records} records into {table_name}")
            except ValueError:
                print("Invalid number of records. Please enter an integer.")
                log_error("Invalid number of records entered.")
        else:
            error_message = (
                f"Table {table_name} does not exist in database {current_db}."
            )
            print(error_message)
            log_error(error_message)
    else:
        error_message = (
            "No database selected. Use the 'use <database_name>' command first."
        )
        print(error_message)
        log_error(error_message)


def handle_desc_table(command, parser, current_db, table_list):
    """Handle the 'desc' command to describe a table."""
    if current_db:
        table_name = parser.get_arg()
        table_list.describe_tables(table_name)
    else:
        error_message = (
            "No database selected. Use the 'use <database_name>' command first."
        )
        print(error_message)
        log_error(error_message)


def handle_show_create_table(command, parser, current_db, table_list):
    """Handle the 'show create table' command."""
    if current_db:
        table_name = parser.get_arg(3)
        if not table_name:
            error_message = "No table name provided for 'show create table' command."
            print(error_message)
            log_error(error_message)
        else:
            try:
                table_list.show_create_table(current_db, table_name)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
    else:
        error_message = "No database selected when attempting to show create table."
        print(error_message)
        log_error(error_message)


def handle_select_all(command, parser, current_db, table_list):
    """Handle the 'select * from' command to select all data from a table."""
    if current_db:
        table_name = parser.get_arg(3)
        if table_name:
            table_list.select_all(table_name)
        else:
            error_message = "No table name provided for 'select all' command."
            print(error_message)
            log_error(error_message)
    else:
        error_message = "No database selected when attempting to select all data."
        print(error_message)
        log_error(error_message)


def handle_custom_syntax(command, table_list):
    """Handle custom syntax like 'table->all()' or 'table->all(<limit>)'."""
    parts = command.split("->")
    if len(parts) == 2:
        table_name = parts[0].strip()
        action_part = parts[1].strip()
        if action_part.startswith("all"):
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
            error_message = f"Invalid action: {action_part}. Use 'table->all()' or 'table->all(<limit>)'."
            print(error_message)
            log_error(error_message)
    else:
        error_message = (
            f"Invalid command: {command}. Type '--help' for a list of commands."
        )
        print(error_message)
        log_error(error_message)


def is_running():
    global query_running
    try:
        """Main function and database handling."""
        db_connection = connect_to_database()
        db_list, table_list, column_information, fake_data = create_managers(
            db_connection
        )
        print(
            f"Welcome to the {Style.BLUE} 'FastInsert' {Style.RESET} Type '--help' or '--h' for help. Type 'exit' to exit"
        )
        current_db = None
        while True:
            try:
                prompt = (
                    f"FastInsert [{current_db}]> " if current_db else "FastInsert> "
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
