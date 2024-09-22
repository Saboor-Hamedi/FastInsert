from faker import Faker
import mysql.connector
from Style import Style
import re
import datetime
from FlashMessage import FlashMessage

flash = FlashMessage()

class FakerDataGenerator:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.faker = Faker()

    def generate_fake_data(self, col_name, col_type, max_length=None):
        """
        Generate fake data based on column name and type.

        Args:
            col_name (str): The name of the column.
            col_type (str): The type of the column.
            max_length (int, optional): The maximum length of the column (for varchar/text).

        Returns:
            str/int/float/bool: The generated fake data.
        """
        col_type = col_type.lower()

        # Keyword matching for column names
        keyword_mapping = {
            "name": lambda _: self.faker.first_name(),
            "lastname": lambda _: self.faker.last_name(),
            "age": lambda _: self.faker.random_int(min=5, max=50),
            "address": lambda _: self.faker.address(),
            "email": lambda _: self.faker.email(),
        }

        # Default type mapping if no keyword match is found
        type_mapping = {
            "varchar": lambda max_length: self.faker.text(max_nb_chars=max_length)[
                :max_length
            ]
            if max_length
            else self.faker.text(),
            "text": lambda max_length: self.faker.text(max_nb_chars=max_length)[
                :max_length
            ]
            if max_length
            else self.faker.text(),
            "timestamp": lambda _: self.faker.date_time_this_decade(),
            "bool": lambda _: self.faker.pybool(),
            "boolean": lambda _: self.faker.pybool(),
            "smallint": lambda _: self.faker.random_int(min=0, max=32767),
            "int": lambda _: self.faker.random_int(min=0),
            "bigint": lambda _: self.faker.random_int(min=0, max=9223372036854775807),
            "decimal": lambda _: self.faker.pydecimal(
                left_digits=10, right_digits=2, positive=True
            ),
            "float": lambda _: self.faker.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            "double": lambda _: self.faker.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
        }

        # Check if there is a keyword match for column name
        for keyword, generator in keyword_mapping.items():
            if re.search(keyword, col_name, re.IGNORECASE):
                return generator(max_length)

        # Check if there is a mapping for column type
        for key in type_mapping:
            if key in col_type:
                return type_mapping[key](max_length)

        return None

    def insert_data(
        self, cnx, cursor, db_name, table_name, num_records, columns, batch_size=10000
    ):
        
        """
        Inserts fake data into a table in the specified database.

        Args:
            cnx (mysql.connector.connection): The database connection object.
            cursor (mysql.connector.cursor): The database cursor object.
            db_name (str): The name of the database.
            table_name (str): The name of the table.
            num_records (int): The number of records to insert.
            columns (list): A list of tuples containing (column_name, column_type, column_length).
        """
        start_time = datetime.datetime.now()
      
        successful_inserts = 0
        failed_inserts = 0
        batch_data = []
        
        cursor.execute('SET foreign_key_checks = 0; ')
        cursor.execute(f"ALTER TABLE {table_name} DISABLE KEYS;")
        for _ in range(num_records):
            data = {}
            columns_to_insert = []

            for col_name, col_type, col_length in columns:
                if col_name.lower() == "id":
                    # Skip the id column if it's auto-incrementing
                    continue
                else:
                    data[col_name] = self.generate_fake_data(
                        col_name, col_type, max_length=col_length
                    )
                    columns_to_insert.append(col_name)

            if not columns_to_insert:
                # No valid columns to insert data into
                continue
            
            
            # create a list of values in the correct order 
            values = [data[col] for col in columns_to_insert]
            batch_data.append(values)
            if len(batch_data) >= batch_size:
                self.insert_in_batch(cursor, table_name, columns_to_insert, batch_data)
                batch_data = []
                successful_inserts += 1
        if batch_data:
            self.insert_in_batch(cursor, table_name, columns_to_insert, batch_data)
        cnx.commit()
        cursor.execute("SET foreign_key_checks = 1;")
        cursor.execute(f"ALTER TABLE {table_name} ENABLE KEYS;")

        self.display_message(
            start_time,
            num_records=num_records,
            successful_inserts=successful_inserts,
            failed_inserts=failed_inserts,
        )

    def insert_in_batch(self, cursor, table_name, columns, batch_data):
        columns_without_id = [col for col in columns if col.lower() != "id"]
        placeholders = ", ".join(["%s"] * len(columns_without_id))
        columns_str = ", ".join(columns_without_id)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        try:
            cursor.executemany(sql, batch_data)
            return len(batch_data)
        except mysql.connector.Error as err:
            flash.error_message(f"{Style.RED}Error inserting batch: {err}{Style.RESET}")

    def display_message(
        self, start_time, num_records=None, successful_inserts=None, failed_inserts=None
    ):
        """
        Display a message based on the number of records inserted.

        Args:
            start_time (datetime.datetime): The start time of the operation.
            num_records (int, optional): The number of records attempted to be inserted.
            successful_inserts (int, optional): The number of records successfully inserted.
            failed_inserts (int, optional): The number of records that failed to be inserted.
        """
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        
        flash.success_message(f"{Style().GREEN}{num_records} rows set in ({elapsed_time}) sec{Style().RESET}")
        
