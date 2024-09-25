# NOTE: 
    # This file is all functions, such as select, all, desc, use, show create table, and so on. \
    # Do you just just rely on this file, you can make your own custom functions.\n
    # It would be better to add them in the same folder to keep things organize, but you are welcome to add them anywhere you wish.
    # If you add them in the same folder, you can import them by using the following:
    # from src.function_name import function_name
    # on the main.py you can just simply add the function name on the command_handler

# show tables
from src.database_show_tables import get_tables

# insert data 
from src.insert_table_data import insert_data

# desc table
from src.show_table_view import get_table_view

# show create table 
from src.show_table_structure import get_table_structure

# select * from table
from src.fetch_star_all import fetch_all

# post::all() || post::all(5)
from src.custom_fetch_all import all

# insert data with foreign key, like table_name::withkey(['user_id' => 1]).single()
from _keys._foreing.foreign_key_data_insertion import insert_data_with_foreign_keys

# handle foreig keys, set 0 || 1 also, like active::foreign_key(0)
# enable::keys(details) || disable::keys(details)
from _keys._constraint.foreign_on_off import contstraint_handler

# use database_name
from src.use_database_selector import switch_database

def use_db(db_list, parser):
    return switch_database(db_list, parser)
    
def show_tables(current_db, table_list):
    return get_tables(current_db, table_list)
def insert(command, parser, current_db,table_list,
    column_information, fake_data,db_connection):
    return insert_data(command, parser, current_db,table_list,
    column_information, fake_data,db_connection)
def desc_table(command, parser, current_db, table_list):
    """
        This fuction is responsible for describing the table
        @param command: This is the command
        @param parser: This is the parser
        @param current_db: This is the current database
        @param table_list: This is the table list
        
        EXAMPLE: 
            >>> desc table_name
    """
    return get_table_view(command, parser, current_db, table_list)
    
def show_create_table(command, parser, current_db, table_list):
    """
    EXAMPLE:
        >>> show create table table_name

        >>> show_create_table(command, parser, current_db, table_list)
        
        DESCRIPTION: 
            Handle the 'show create table' command to show the create table statement.\n
            The actual function is on the src/show_table_structure.py\n
    """
    return get_table_structure(command, parser, current_db, table_list)

def select_all(command, table_list):
    """
    DESCRIPTION:
    This function is responsible to select * from table_name.
    This is a custom function, which is not in the official mysql client.

    EXAMPLE:
        >>> table_name::all() without limit
        >>> table_name::(11) with limit
                     
    """
    return all(command, table_list)

def fetch_all_from_table(command, parser, current_db, table_list):
    """
    This function is responsible to fetch data, like select * from table_name.

    @param command: This is the a command
    @param parser: This is the parser
    @param current_db: This is the current database
    @param table_list: This is the table list
    
    """
    return fetch_all(command, parser, current_db, table_list)


def insert_foreign_key(command, current_db, table_list, column_information, fake_data, db_connection):
    """
    This function is responsible to insert data with foreign key.
    @param command: This is the command
    @param current_db: This is the current database
    @param table_list: This is the table list
    @param
    column_information: This is the column information
    fake_data: This is the fake data
    db_connection: This is the database connection

        EXAMPLE:
            >>> table_name::withkey(['post_id' => 1]).single()
            >>> table_name::withkey(['user_id' => 1,'post_id' => 1]).single()
        
    """
    return insert_data_with_foreign_keys(command, current_db, table_list, column_information, fake_data, db_connection)
    


def active_foreign_key(command, current_db, db_connection):
    
    """
        This function is responsible to enable or disable foreign key checks.
        @param command: This is the command
        @param current_db: This is the current database
        @param db_connection: This is the database connection
        
        EXAMPLE:
            >>> active::foreign_key(0)
            >>> active::foreign_key(1)
    """
    
    
    return contstraint_handler(command, current_db, db_connection)