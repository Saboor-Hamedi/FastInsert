
class HandleKeys:

    def __init__(self, db_connection):
        
        """
        Initializes the HandleKeys object with a database connection.

        Args:
            db_connection (dict): A dictionary containing a database connection
                object and a cursor object.
        """
        self.db_connection = db_connection
    def enable_keys(self,table_name):
        cursor = self.db_connection['cursor']
        cursor.execute(f'ALTER TABLE {table_name} ENABLE KEYS;')

    def disable_keys(self,table_name):
        cursor = self.db_connection['cursor']
        cursor.execute(f'ALTER TABLE {table_name} DISABLE KEYS;')
        
    def disable_foreign_keys(self):
        cursor = self.db_connection['cursor']
        cursor.execute('SET foreign_key_checks = 0;')
    def enable_foreign_keys(self):
        cursor = self.db_connection['cursor']
        cursor.execute('SET foreign_key_checks = 1;')