
from Style import Style
from tabulate import tabulate

from reports import terminated_app
class ColumnManager:
    def __init__(self, cursor):
        self.cursor = cursor

    """
        Get all columns which is in the selected table, also select database 
    """

    def get_column_information(self, db_name, table_name):
        db_name = db_name.lower()
        table_name = table_name.lower()
        self.cursor.execute(f"USE {db_name}")
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
    
    def describe_tables(self, table_name):
        try:
            self.cursor.execute(f'DESCRIBE {table_name}')
            columns = self.cursor.fetchall()
            if not columns:
                print(f"{Style.RED}Table '{table_name}' does not exist.{Style.RESET}") 
                return 
            print(f"{Style.YELLOW}Table: {table_name}{Style.RESET}")
            print(tabulate(columns, headers=['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'], tablefmt='psql'))
        except Exception as e:
            print(f"{Style.RED} An error occured: {str(e)} {e}{Style.RESET}")
            terminated_app(f"{Style.RED} An error occurred while describing the table {table_name}: {str(e)} {Style.RESET}")

            
            

        
