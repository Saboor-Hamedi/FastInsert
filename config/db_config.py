from get_user_input import create_managers, connect_to_database

def initialize():
    db_connection = connect_to_database()
    db_list, table_list, column_information, fake_data = create_managers(db_connection)
    return db_connection, db_list, table_list, column_information, fake_data