from _keys._constraint.HandleKeys import HandleKeys
from FlashMessage import FlashMessage
flash = FlashMessage()
def contstraint_handler(command, current_db, db_connection):
    if not current_db:
        flash.error_message(
            "No database selected. Use the 'use <database_name>' command first.",
            "No database selected.",
        )
        return
    try:
        handl_keys = HandleKeys(db_connection)
        if command == "active::foreign_key(0)":
            handl_keys.disable_foreign_keys()  # Disable foreign key checks in DB
            flash.success_message("Foreign key checks disabled.")
        elif command == "active::foreign_key(1)":
            handl_keys.enable_foreign_keys()  # Enable foreign key checks in DB
            flash.success_message("Foreign key checks enabled.")
        elif command.startswith("enable::keys("):
            table_name = command.split("enable::keys(")[-1].strip(")")
            handl_keys.enable_keys(table_name)
            flash.success_message(
                f"Keys enabled for table {table_name}.",
                f"Keys enabled for table {table_name}.",
            )
        elif command.startswith("disable::keys("):
            table_name = command.split("disable::keys(")[-1].strip(")")
            handl_keys.disable_keys(table_name)
            flash.success_message(
                f"Keys disabled for table {table_name}.",
                f"Keys disabled for table {table_name}.",
            )
        else:
            flash.error_message(
                "Invalid syntax. Use 'active::foreign_key(0)' or 'active::foreign_key(1)'"
            )
        return current_db
    except Exception as err:
        flash.error_message(f"Something went wrong with the key {err}")