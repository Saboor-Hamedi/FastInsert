
from tabulate import tabulate

class DatabaseManager:
    """
    Manages database operations.
    """
    def __init__(self, cursor):
        """
        Initializes the DatabaseManager with a cursor object.

        Args:
            cursor: A cursor object for database interactions.
        """
        self.cursor = cursor

    def get_database_list(self):
       
        """
        Retrieves a list of existing databases from the MySQL server.
        A table is printed out with the database names and their corresponding numbers.
        The list of database names is returned.

        Returns:
            list: A list of database names.
        """
        self.cursor.execute("SHOW DATABASES")
        database = self.cursor.fetchall()
        
        """Extract the db_names"""
        db_names = [db[0] for db in database]
        
        """create a create tabulate"""   
        table_data =  [(index + 1, db_name) for  index, db_name in enumerate(db_names)]
        headers = ['No', 'Database Names']
        print(tabulate(table_data, headers, tablefmt='psql'))
        return db_names
    
    def select_database(self, db_name):
        
        """
        Selects a database to use for subsequent database operations.

        Args:
            db_name (str): The name of the database to select.

        Raises:
            mysql.connector.Error: If the database does not exist.
        """
        self.cursor.execute(f'USE {db_name}')
        print(f'Database selected: {db_name}')
        # try:
        # except mysql.connector.Error as err:
        #     print(f'Unknown database {err}')
        #     log_error('This {Style.RED} {db_name} does not exits {Style.RESET}')
    def get_existing_databases(self):
        """
        Retrieves a list of all existing databases in the MySQL server.

        Returns:
            list: A list of database names.
        """
        self.cursor.execute("SHOW DATABASES")
        database = self.cursor.fetchall()
        
        """Extract the db_names"""
        db_names = [db[0] for db in database]
        
        return db_names

    def check_database(self, db_name):
        """
            Checks if the specified database exists in the MySQL server.

            Args:
                db_name (str): The name of the database to check.

            Returns:
                bool: True if the database exists, False otherwise.
        """
        db_name = db_name.lower()
        if db_name in self.get_existing_databases():
            return True
        else:
            return False
    
    