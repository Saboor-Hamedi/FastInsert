from FlashMessage import FlashMessage
import mysql.connector
flash = FlashMessage()
def get_table_structure(command, parser, current_db, table_list):
    """Handle the 'show create table' command."""
    if current_db:
        table_name = parser.get_arg(3)
        if not table_name:
            flash.error_message(
                "No table name provided for 'show create table' command.",
                "No table name provided for 'show create table' command.",
            )
        else:
            try:
                table_list.show_create_table(current_db, table_name)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
    else:
        flash.error_message(
            "No database selected when attempting to show create table.",
            "No database selected when attempting to show create table.",
        )
