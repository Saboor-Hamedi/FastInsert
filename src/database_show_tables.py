from FlashMessage import FlashMessage
import mysql.connector

flash = FlashMessage()

def get_tables(current_db, table_list):
    try:
        if current_db:
            return table_list.show_tables(current_db)
        else:
            flash.error_message(
                "ERROR 1046 (3D000): No database selected",
                "No database selected when attempting to show tables",
            )
    except mysql.connector.Error as err:
        flash.error_message(f"{err}", "This {current_db} is not exists")
    except Exception as err:
        flash.error_message(f"{err}", "This {current_db} is not exists")
