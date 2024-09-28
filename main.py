import sys
from get_user_input import display_help
from CommandParser import CommandParser
from FlashMessage import FlashMessage

#  initialize the database connection
from config.db_config import initialize

# commands
from commands.command_handler import (
    use_db,  # use db
    show_tables,  # show tables
    insert,  # insert table_name
    desc_table,  # desc table table_name
    show_create_table,  # show create table table_name
    select_all,  # select * from table_name
    fetch_all_from_table,  # select * from table_name
    insert_foreign_key,  # insert foreign key
    active_foreign_key,  # active_foreign_key,
    truncate_table,  # truncate table
)

flash = FlashMessage()


def execute_command(
    command_input,
    db_list,
    table_list,
    column_information,
    fake_data,
    db_connection,
    current_db,
):
    """Execute a command based on user input."""
    parser = CommandParser(command_input)
    command = parser.get_command()

    if command == "show databases":
        db_list.get_database_list()

    elif command.startswith("use "):
        return use_db(db_list, parser)
    elif command == "show tables":
        show_tables(current_db, table_list)
    elif command.startswith("insert "):
        insert(
            command,
            parser,
            current_db,
            table_list,
            column_information,
            fake_data,
            db_connection,
        )
    elif command.startswith("desc "):
        desc_table(command, parser, current_db, table_list)
    elif command.startswith("show create table"):
        show_create_table(command, parser, current_db, table_list)
    elif command.startswith("select * from"):
        try:
            fetch_all_from_table(
                command, parser, current_db, table_list
            )  # select * from table_name
        except Exception as e:
            flash.error_message(f"An error occurred: {e}")
        finally:
            return False
    elif "::withkey(" in command and (
        ").length(" in command or ").single()" in command
    ):
        insert_foreign_key(
            command,
            current_db,
            table_list,
            column_information,
            fake_data,
            db_connection,
        )
    elif command.startswith("active::"):
        return active_foreign_key(command, current_db, db_connection)
    elif command.startswith("enable::") or command.startswith("disable::"):
        return active_foreign_key(command, current_db, db_connection)
    elif "::truncate()" in command:
        truncate_table(command, db_connection)
    elif "::truncate()" in command:
        truncate_table(command, db_connection)
    elif "::" in command:
        select_all(command, table_list)  # fetch all data post::all() || post::all(10)
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
    try:
        db_connection, db_list, table_list, column_information, fake_data = (
            initialize()
        )  # initizlize the database connection config/db_config

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
        else:
            print(f"An error occurred: {e}")
    finally:
        sys.exit(0)


def main():
    is_running()


if __name__ == "__main__":
    main()
