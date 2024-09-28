from datetime import datetime
from _keys._constraint.HandleKeys import HandleKeys
from FlashMessage import FlashMessage

flash = FlashMessage()


def contstraint_handler(command, current_db, db_connection):
    start_time = datetime.now()
    successful_inserts = 0

    """
        This function is responsible to enable or disable foreign key checks.
        @param command: This is the command
        @param current_db: This is the current database
        @param db_connection: This is the database connection
        
        EXAMPLE:
            >>> active::foreign_key(0)
            >>> active::foreign_key(1)
        
    """

    start_time = datetime.now()
    if not current_db:
        flash.error_message(
            "No database selected. Use the 'use <database_name>' command first.",
            "No database selected.",
        )
        return
    try:
        handl_keys = HandleKeys(db_connection)
        successful_inserts += 1
        if command == "active::foreign_key(0)":
            handl_keys.disable_foreign_keys()  # Disable foreign key checks in DB
            flash.set_keys_message(
                "Query OK, 0 rows affected", start_time, success=True
            )
        elif command == "active::foreign_key(1)":
            handl_keys.enable_foreign_keys()  # Enable foreign key checks in DB
            flash.set_keys_message(
                "Query OK, 0 rows affected", start_time, success=True
            )
        elif command.startswith("enable::keys("):
            table_name = command.split("enable::keys(")[-1].strip(")")
            handl_keys.enable_keys(table_name)
            flash.set_keys_message(
                "Query OK, 0 rows affected", start_time, success=True
            )

        elif command.startswith("disable::keys("):
            table_name = command.split("disable::keys(")[-1].strip(")")
            handl_keys.disable_keys(table_name)
            flash.set_keys_message(
                "Query OK, 0 rows affected", start_time, success=True
            )
        else:
            flash.error_message(
                "Invalid syntax. Use 'active::foreign_key(0)' or 'active::foreign_key(1)'"
            )
        return current_db

    except Exception as err:
        flash.error_message(f"Something went wrong with the key {err}")
