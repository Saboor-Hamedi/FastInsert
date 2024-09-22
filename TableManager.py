from Style import Style
from tabulate import tabulate
from loggin import log_error
import mysql.connector
from datetime import datetime
import time

from FlashMessage import FlashMessage

flash = FlashMessage()
class TableManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def show_tables(self, db_name):
        try:
            self.cursor.execute(f"USE {db_name}")
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            if not tables:
                print(f"No table found in {db_name}")
                return []
            table_list = [
                [i + 1, table[0]] for i, table in enumerate(tables)
            ]  # show with no, and table
            print(
                tabulate(table_list, headers=["No", db_name.upper()], tablefmt="psql")
            )
            return [table[0] for table in tables]

        except mysql.connector.Error as err:
            flash.error_message(f"No database selected when attempting to show tables {err}", "No database selected when attempting to show tables")
        except Exception as e:
            print(f"An error occured: {e}")
            flash.error_message(f"An error occured: {e}")
            flash.error_message("Something went wront with the table name", "Something went wront with the table name")
            return []

    def show_create_table(self, db_name, table_name):
        try:
            if not db_name:
                flash.success_message("Please provide a database name.")
                return ""

            # Check if the database exists
            self.cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in self.cursor.fetchall()]
            if db_name not in databases:
                flash.error_message(f"Database {db_name} does not exist.")
                return ""
            # Use the specified database
            self.cursor.execute(f"USE {db_name}")

            if not table_name:
                flash.error_message("No table name provided. Use 'show create table <table_name>",f"No table name provided. Use {Style.BLUE}'show create table <table_name>'{Style.RESET}.")
                return ""

            # Check if the table exists
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not self.cursor.fetchall():
                print(
                    f"Table {Style.RED}{table_name}{Style.RESET} not found in {db_name}"
                )
                return ""

            # Get the CREATE TABLE statement
            self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
            result = self.cursor.fetchone()
            if not result:
                flash.error_message(f"Could not retrieve CREATE TABLE statement for {table_name}.")
                return ""
            create_table_stmt = result[1]
            # print(f"CREATE TABLE statement for {table_name} \n{create_table_stmt}")
            flash.success_message(f"CREATE TABLE statement for {table_name} \n{create_table_stmt}")
            return create_table_stmt

        except mysql.connector.Error as err:
            log_error(f"{Style.RED}Database error: {err}{Style.RESET}")
            flash.error_message(f"Database error: {err}", f"Database error: {err}")
            return ""

        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            flash.error_message(f"An unexpected error occurred: {err}",f"Something went wrong while retrieving the CREATE TABLE statement for {table_name}")
            return ""

    def describe_tables(self, table_name):
        try:
            self.cursor.execute(f"DESCRIBE {table_name}")
            records = self.cursor.fetchall()
            if not records:
                flash.error_message(f"Table '{table_name}' does not exist")
                return
            flash.success_message(f"Table: {table_name}")
            print(tabulate(records, headers=self.cursor.column_names, tablefmt="psql"))
        except Exception as e:
            flash.error_message(f"An error occured: {str(e)} {e}", f" An error occurred while describing the table {table_name}: {str(e)}")

    def execute_quer(self, query):
        cursor = self.cursor
        cursor.execute(query)
        return cursor.fetchall()

    # select table
    def select_all(self, table_name):
        start_time = time.time()

        try:
            # Use parameterized query to prevent SQL injection
            query = f"SELECT * FROM `{table_name}`"
            records = self.execute_quer(query)
            end_time = time.time()
            if not records:
                flash.error_message(f"No record found in {table_name}")
                return ""
            # pandas atble
            print(tabulate(records, headers=self.cursor.column_names, tablefmt="psql"))
            num_records = len(records)
            if num_records > 1:
                flash.success_message(f"{num_records} rows in set")
            elif num_records == 1:
                flash.success_message(f"{num_records} row in set")
            else:
                flash.success_message(f"{num_records} row in set")
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.3f} seconds")
            start_time_dt = datetime.fromtimestamp(start_time)
            end_time_dt = datetime.fromtimestamp(end_time)
            self.show_time_duration("Time:", start_time_dt, end_time_dt)

            return records
        except mysql.connector.Error as err:
            flash.error_message(f"Database error: {err}")
        except Exception as err:
            flash.error_message(f"An unexpected error occurred: {err}")

    def all(self, table_name, limit=None):
        start_time = time.time()
        try:
            # Use parameterized query to prevent SQL injection
            if limit is not None:
                query = f"SELECT * FROM `{table_name}` LIMIT {limit}"
            else:
                query = f"SELECT * FROM `{table_name}`"

            records = self.execute_quer(query)
            end_time = time.time()
            if not records:
                flash.error_message(f"No record found in {table_name}")
                return ""
            # Display data if found
            print(tabulate(records, headers=self.cursor.column_names, tablefmt="psql"))
            execution_time = end_time - start_time
            flash.success_message(f"Execution time: {execution_time:.3f} seconds")
            start_time_dt = datetime.fromtimestamp(start_time)
            end_time_dt = datetime.fromtimestamp(end_time)
            self.show_time_duration("Time:", start_time_dt, end_time_dt)
            return records
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash.error_message(f"Database error: {err}")
        except Exception as err:
             flash.error_message(f"An unexpected error occurred: {err}", f"An unexpected error occurred: {err}")

    def show_time_duration(self, prefix, start_time, end_time):
        time_diff = end_time - start_time
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        flash.success_message(f"{prefix} {hours:02}:{minutes:02}:{seconds:02}.{time_diff.microseconds:06}")