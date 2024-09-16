import mysql.connector
from Style import Style
class DatabaseConnection:
    def __init__(self, host, user, password, port=3306, collation='utf8mb4_unicode_ci'):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.collation = collation
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                port=self.port, 
                collation=self.collation)
            self.cursor = self.connection.cursor()
            print(f'{Style.BLUE}Connection successfully made.{Style.RESET}')
            return True
        except mysql.connector.Error as err:
            print(f'Connection failed: {err}')
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
    
    def commit(self):
        if self.connection:
            self.connection.commit()
        else:
            raise RuntimeError("No connection to commit.")
