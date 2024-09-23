import datetime
import mysql.connector
from FakerDataGenerator import FakerDataGenerator
from FlashMessage import FlashMessage
from ColumnManager import ColumnManager
class HandleForeingKey:
    def __init__(self, db_connection, table_name, key_dict):
        self.db_connection = db_connection
        self.table_name = table_name
        self.key_dict = key_dict
        self.fakeGen = FakerDataGenerator(self.db_connection)
        self.column_manager = ColumnManager(self.db_connection['cursor'])   
        self.flash = FlashMessage()

    start_time = datetime.datetime.now()
    def insert_data_with_keys(self, cnx, cursor, db_name, table_name, num_records, columns, key_dict):

        successful_inserts = 0
        failed_inserts = 0
        
        columns = self.column_manager.get_column_information(db_name, self.table_name)
        if not self.validate_keys(columns):
            self.flash.error_message("One or more foreign key columns are invalid.")
            return
        for _ in range(num_records):
            data, columns_to_insert = self.prepare_data(columns)  
            
            if not columns_to_insert:
                continue
            
            try:
                self.insert_records(db_name, data, columns_to_insert)
                successful_inserts += 1
            except mysql.connector.Error as err:
                self.flash.error_message(f"Error inserting data: {err}")
                cnx.rollback()
                failed_inserts += 1

        self.flash.exucation_message(
            self.start_time,
            num_records=num_records,
            success=successful_inserts,
            failed=failed_inserts,
        )
    def validate_keys(self, columns):
        """
        Validates if the keys provided in key_dict are valid columns in the table.

        Args:
            columns (list): List of tuples containing column information (name, type, length).

        Returns:
            bool: True if all keys are valid columns, False otherwise.
        """
        column_names = [col[0].lower() for col in columns]
        for key in self.key_dict:
            if key.lower() not in column_names:
                return False
        return True

    def prepare_data(self, columns):
        data = {}
        columns_to_insert = []

        for col_name, col_type, col_length in columns:
            if col_name.lower() in self.key_dict:
                data[col_name] = self.key_dict[col_name]
            else:
                data[col_name] = self.fakeGen.generate_fake_data(col_name, col_type, max_length=col_length)
            columns_to_insert.append(col_name)

        return data, columns_to_insert
    def insert_records(self, db_name, data, columns_to_insert):
        cursor  = self.db_connection['cursor']
        placeholders  = ', '. join(['%s'] * len(data))
        columns_str = ', '.join(data.keys())
        sql = f"INSERT INTO {db_name}.{self.table_name} ({columns_str}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        self.db_connection['cnx'].commit()
    
    
    
