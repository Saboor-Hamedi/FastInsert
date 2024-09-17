import sys
from FakeData import FakeData
from ListDatabase import ListDatabase
from ListTable import ListTable
from ListColumns import ListColumns

# from input_utils import prompt_for_input, validate_port
from get_user_input import (
    get_user_input,initialize_database_connection
)

def main():
    """Main function and database handling"""
    try:
        cnx = initialize_database_connection()
        db_list = ListDatabase(cnx.cursor)
        table_list = ListTable(cnx.cursor)
        all_columns = ListColumns(cnx.cursor)
        fake_data = FakeData(cnx)

        while True:
            option = get_user_input()
            if option == "1":
                db_list.list_databases()
            elif option == "2":
                databases = [db.lower() for db in db_list.list_databases()]
                db_name = input("Enter the name of the database to select: ")
                if db_name.lower() in databases:
                    while True:
                        print(f"\nSelected database: {db_name}")
                        print("[1] List tables")
                        print("[2] Select table")
                        print("[0] Go back")
                        sub_option = input("Enter your choice: ")
                        if sub_option == "1":
                            table_list.list_tables(db_name)
                        elif sub_option == "2":
                            tables = [
                                table.lower()
                                for table in table_list.list_tables(db_name)
                            ]
                            table_name = input(
                                "Enter the name of the table to select: "
                            )
                            if table_name.lower() in tables:
                                columns = all_columns.all_columns(db_name, table_name)
                                print(f"Columns in {table_name}:")
                                for col in columns:
                                    print(f"  - {col[0]} ({col[1]})")
                                num_records = int(
                                    input("Enter the number of records to insert: ")
                                )
                                fake_data.insert_data(
                                    cnx,
                                    cnx.cursor,
                                    db_name,
                                    table_name,
                                    num_records,
                                    columns,
                                )
                            else:
                                print(
                                    f"Table {table_name} does not exist in database {db_name}."
                                )
                        elif sub_option == "0":
                            break
                        else:
                            print("Invalid option. Please try again.")
                else:
                    print(f"Database {db_name} does not exist.")
            elif option == "0":
                break
            else:
                print("Invalid option. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
