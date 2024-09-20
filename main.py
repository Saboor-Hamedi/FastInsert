from Style import Style
import mysql.connector
from get_user_input import connect_to_database, create_managers, display_help
from reports import success_report, terminated_app

def main():
    """Main function and database handling"""
    db_connection = connect_to_database()
    db_list, table_list, column_information, fake_data = create_managers(db_connection)
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
                terminated_app(f"Attemp to use that database {db_name} does not exists")
        elif command == "show tables":
            if current_db:
                table_list.show_tables(current_db)
            else:
                print(
                    "No database selected. Use the 'use <database_name>' command first."
                )
                terminated_app("No database selected when attempting to show tables")
        elif command.startswith("table "):
            if current_db:
                table_name = command.split(" ", 1)[1]
                tables = [table.lower() for table in table_list.show_tables(current_db)]
                if table_name in tables:
                    columns = column_information.get_column_information(
                        current_db, table_name
                    )
                    print(f"columns in {table_name}")
                    for col in columns:
                        print(f" - {col[0]} ({col[1]})")
                    try:
                        num_records = int(
                            input("Enter the number of records to insert: ")
                        )
                        fake_data.insert_data(
                            db_connection["cnx"],
                            db_connection["cursor"],
                            current_db,
                            table_name,
                            num_records,
                            columns,
                        )
                        success_report(
                            f"Inserted {num_records} records into {table_name}"
                        )
                    except ValueError:
                        print("Invalid number of records. Please enter an integer.")
                        terminated_app("Invalid number of records entered.")
                else:
                    print(
                        f"Table {table_name} does not exist in database {current_db}."
                    )
                    terminated_app(
                        f"Attempted to select a non-existent table: {table_name}"
                    )
            else:
                print(
                    "No database selected. Use the 'use <database_name>' command first."
                )
                terminated_app(
                    "No database selected when attempting to select a table."
                )
        elif command.startswith("desc "):
            if current_db:
                table_name = command.split(" ", 1)[1]
                column_information.describe_tables(table_name)
            else:
                print(
                    "No database selected. Use the 'use <database_name>' command first."
                )
                terminated_app(
                    "No database selected when attempting to describe a table."
                )
        elif command.startswith("show create table"):
            if current_db:
                parts = command.split(" ", 3)
                table_name = parts[3] if len(parts) > 3 else None
                try:
                    table_list.show_create_table(current_db, table_name)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
            else:
                print(
                    "No database selected. Use the 'use <database_name>' command first."
                )
                terminated_app(
                    "No database selected when attempting to show create table."
                )
        elif command == "--help" or command == "--h":
            display_help()
        elif command == "exit":
            success_report("Exit command executed. Application terminating.")
            break
        else:
            print(f"Invalid command: {command}. Type '--help' for a list of commands.")
            terminated_app(f"Invalid command entered: {command}")


if __name__ == "__main__":
    main()
