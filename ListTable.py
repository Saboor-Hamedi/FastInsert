

class ListTable:
    
    def __init__(self, cursor):
        self.cursor = cursor
        
    def list_tables(self, db_name):
        self.cursor.execute(f"USE {db_name}")
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        if tables:
            print(f"Tables in {db_name}:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print(f"No tables found in {db_name}")
        return [table[0] for table in tables]