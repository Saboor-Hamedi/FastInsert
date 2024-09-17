from faker import Faker
import mysql.connector
from Style import Style
import re

class FakeData:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.faker = Faker()

    def generate_fake_data(self, col_name, col_type, max_length=None):
        col_type = col_type.lower()
        
        """Keyword matching for column names"""
        keyword_mapping = {
            "name": lambda _: self.faker.first_name(),
            "lastname": lambda _: self.faker.last_name(),
            "age": lambda _: self.faker.random_int(min=5, max=50),
            "address": lambda _: self.faker.address(),
            "email": lambda _: self.faker.email(),
        }

        """Default type mapping if no keyword match is found"""
        type_mapping = {
            "varchar": lambda max_length: self.faker.text(max_nb_chars=max_length)[:max_length] if max_length else self.faker.text(),
            "text": lambda max_length: self.faker.text(max_nb_chars=max_length)[:max_length] if max_length else self.faker.text(),
            "timestamp": lambda _: self.faker.date_time_this_decade(),
            "bool": lambda _: self.faker.pybool(),
            "boolean": lambda _: self.faker.pybool(),
            "smallint": lambda _: self.faker.random_int(min=0, max=32767),
            "int": lambda _: self.faker.random_int(min=0),
            "bigint": lambda _: self.faker.random_int(min=0, max=9223372036854775807),
            "decimal": lambda _: self.faker.pydecimal(left_digits=10, right_digits=2, positive=True),
            "float": lambda _: self.faker.pyfloat(left_digits=5, right_digits=2, positive=True),
            "double": lambda _: self.faker.pyfloat(left_digits=5, right_digits=2, positive=True),
        }

        """Check if there is a keyword match for column name"""
        for keyword, generator in keyword_mapping.items():
            if re.search(keyword, col_name, re.IGNORECASE):
                return generator(max_length)

        """Check if there is a mapping for column type"""
        for key in type_mapping:
            if key in col_type:
                return type_mapping[key](max_length)

        return None

    def insert_data(self, cnx, cursor, db_name, table_name, num_records, columns):
        """Inserts fake data into a table in the specified database.
        Args:
            cnx (mysql.connector.connection): The database connection object.
            cursor (mysql.connector.cursor): The database cursor object.
            db_name (str): The name of the database.
            table_name (str): The name of the table.
            num_records (int): The number of records to insert.
            columns (list): A list of tuples containing (column_name, column_type, column_length).
        """
        cursor.execute(f"USE {db_name}")
        for _ in range(num_records):
            data = {}
            columns_to_insert = []
            for col_name, col_type, col_length in columns:
                if col_name == "id" and "auto_increment" in col_type.lower():
                    """Skip the id column if it's auto-incrementing"""
                    continue
                else:
                    data[col_name] = self.generate_fake_data(col_name, col_type, max_length=col_length)
                    columns_to_insert.append(col_name)

            placeholders = ", ".join(["%s"] * len(data))
            columns_str = ", ".join(columns_to_insert)
            sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            try:
                cursor.execute(sql, list(data.values()))
            except mysql.connector.errors.IntegrityError as err:  # noqa: F841
                """Don't print the duplicate entry error message"""
                continue  # Skip this record and move to the next
        cnx.commit()

        print(f"{Style.GREEN}Inserted {num_records} records into {table_name} {Style.RESET}")

