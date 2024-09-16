class ListDatabase:
    def __init__(self, cursor):
        self.cursor = cursor

    def list_databases(self):
        """
        Lists all databases in the MySQL server
        """
        self.cursor.execute("SHOW DATABASES")
        database = self.cursor.fetchall()

        print("Databases: ")
        for db in database:
            print(f" - {db[0]}")
        db_list = [db[0].lower() for db in database]
        return db_list

    def check_database(self, db_name):
        db_name = db_name.lower()
        if db_name in self.list_databases():
            return True
        else:
            return False
