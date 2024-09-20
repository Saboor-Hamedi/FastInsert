from os import terminal_size
from Style import Style
from tabulate import tabulate
from reports import terminated_app
import mysql.connector
# show tables
class TableManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def show_tables(self, db_name):
        """
        List all tables in the specified database.

        Args:
            db_name (str): The name of the database.

        Returns:
            list: A list of table names in the database.
        """
        try:
            self.cursor.execute(f"USE {db_name}")
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            if not tables:
                print(f"No table found in {db_name}")
                return []
            # table_list = [[table[0]] for table in tables] # show  only table names
            table_list = [
                [i + 1, table[0]] for i, table in enumerate(tables)
            ]  # show with no, and table

            print(
                tabulate(table_list, headers=["No", db_name.upper()], tablefmt="psql")
            )

            return [table[0] for table in tables]
        except Exception as e:
            print(f"An error occured: {e}")
            terminated_app(
                f"{Style.RED}Something went wront with the table name{Style.RESET}"
            )
            return []

    def show_create_table(self, db_name, table_name):
        try:
            if not db_name:
                print("Please provide a database name.")
                return ""
                
            # Check if the database exists
            self.cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in self.cursor.fetchall()]
            if db_name not in databases:
                print(f"Database {db_name} does not exist.")
                return ""
                
            # Use the specified database
            self.cursor.execute(f'USE {db_name}')
            
            if not table_name:
                print(f"No table name provided. Use {Style.BLUE}'show create table <table_name>'{Style.RESET}.")
                terminated_app(f'No table name  provided. Use {Style.BLUE} "show create table <table_name>" {Style.RESET}.')
                return ""
                
            # Check if the table exists
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not self.cursor.fetchall():
                print(f"Table {table_name} not found in {db_name}")
                return ""
                
            # Get the CREATE TABLE statement
            self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
            result = self.cursor.fetchone()
            if not result:
                print(f"Could not retrieve CREATE TABLE statement for {table_name}.")
                return ""
                
            create_table_stmt = result[1]
            print(f"CREATE TABLE statement for {table_name} \n{create_table_stmt}")
            return create_table_stmt
        
        except mysql.connector.Error as err:
            terminated_app(f"{Style.RED}Database error: {err}{Style.RESET}")
            return ""
        
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            terminated_app(f"{Style.RED}Something went wrong while retrieving the CREATE TABLE statement for {table_name}{Style.RESET}")
            return ""

