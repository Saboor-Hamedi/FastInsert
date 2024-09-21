
class ColumnManager:
    def __init__(self, cursor):
        """
        Initializes the ColumnManager with a database cursor.

        Args:
            cursor (mysql.connector.Cursor): A cursor object for interacting with the database.
        """
        self.cursor = cursor

    def get_column_information(self, db_name, table_name):
        
       
        """
        Retrieves column information for a specified table in a database.

        Args:
            db_name (str): The name of the database to query for column information.
            table_name (str): The name of the table to retrieve column information for.

        Returns:
            list: A list of tuples containing column name, column type, and column length (where applicable).
        """
        
        db_name = db_name.lower()
        table_name = table_name.lower()
        self.cursor.execute(f"USE {db_name}")
        self.cursor.execute(f"DESCRIBE {table_name}")
        columns = self.cursor.fetchall()
        column_info = []
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            # Extract column length for VARCHAR or TEXT types
            if "varchar" in col_type:
                col_length = int(col_type.split("(")[1].split(")")[0])  # Extract length
            else:
                col_length = None
            column_info.append((col_name, col_type, col_length))
        return column_info
    
   

            
            

        
