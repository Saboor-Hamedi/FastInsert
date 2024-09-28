# truncate table from database
from FlashMessage import FlashMessage
from _keys._delete.Truncate import Truncate

flash = FlashMessage()

def delete_all_data(command, db_connection):
    table_name = command.split("::")[0]
    truncater = Truncate(db_connection)
    truncater.truncate_table(table_name)
    return
