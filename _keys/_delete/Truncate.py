
class Truncate:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def truncate_table(self, table_name):
        cursor = self.db_connection['cursor']
        try:
            cursor.execute(f'TRUNCATE TABLE {table_name};')
            self.db_connection['cnx'].commit()
            print(f"Table {table_name} truncated successfully.")
        except Exception as e:
            print(f"Failed to truncate table {table_name}. Error: {e}")
        