from FlashMessage import FlashMessage

flash = FlashMessage()


def insert_data(
    command,
    parser,
    current_db,
    table_list,
    column_information,
    fake_data,
    db_connection,
):
    """Handle the 'table' command to insert data."""
    if current_db:
        # table_name = command.split(" ", 1)[1]
        table_name = parser.get_arg()
        tables = [table.lower() for table in table_list.show_tables(current_db)]
        if table_name in tables:
            columns = column_information.get_column_information(current_db, table_name)
            # print(f"columns in {table_name}") # show columns
            # for col in columns:
            #     print(f" - {col[0]} ({col[1]})")
            try:
                num_records = int(input("Enter the number of records to insert: "))
                fake_data.insert_data(
                    db_connection["cnx"],
                    db_connection["cursor"],
                    current_db,
                    table_name,
                    num_records,
                    columns,
                )
                flash.success_message(
                    f"Inserted {num_records} records into {table_name}",
                    f"Inserted {num_records} records into {table_name}",
                )
            except ValueError:
                flash.error_message(
                    "Invalid number of records. Please enter an integer.",
                    "Invalid number of records entered.",
                )
        else:
            flash.error_message(
                f"Table {table_name} does not exist in database {current_db}."
            )

    else:
        flash.error_message(
            "No database selected. Use the 'use <database_name>' command first.",
            "No database selected. Use the 'use <database_name>' command first.",
        )
