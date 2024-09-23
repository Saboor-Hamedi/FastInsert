from FlashMessage import FlashMessage
from _keys._foreing.HandleForeingKey import HandleForeingKey
import re
flash = FlashMessage()
def insert_data_with_foreign_keys(
    command, current_db, table_list, column_information, fake_data, db_connection
):
    """Handle the custom insert command with foreign keys."""
    if not current_db:
        flash.error_message(
            "No database selected. Use the 'use <database_name>' command first.",
            "No database selected.",
        )
        return
    try:
        table_name = command.split("::")[0]
        # Parse withkey part
        key_part_match = re.search(r"::withkey\(\[(.*?)\]\)", command)
        if not key_part_match:
            flash.error_message("Invalid syntax for withkey part.")
            return
        key_part = key_part_match.group(1)
        key_dict = {}
        for pair in key_part.split(","):
            key, value = pair.strip().split("=>")
            key_dict[key.strip().strip("'").strip('"')] = int(value.strip())

        # Check for .single() or .length(n) part
        length_match = re.search(r"\.length\((\d+)\)", command)
        single_match = re.search(r"\.single\(\)", command)
        if length_match:
            num_records = int(length_match.group(1))
        elif single_match:
            num_records = 1
        else:
            flash.error_message("Invalid syntax for length or single part.")
            return
        # tables = [table.lower() for table in table_list.show_tables(current_db)]
        if table_name:
            foreignKey = HandleForeingKey(db_connection, table_name, key_dict)
            columns = column_information.get_column_information(current_db, table_name)
            foreignKey.insert_data_with_keys(
                db_connection["cnx"],
                db_connection["cursor"],
                current_db,
                table_name,
                num_records,
                columns,
                key_dict,
            )
        else:
            flash.error_message(
                f"Table {table_name} does not exist in database {current_db}."
            )
    except Exception as e:
        flash.error_message(f"An error occurred: {e}")