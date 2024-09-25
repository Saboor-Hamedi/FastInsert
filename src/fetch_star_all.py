from FlashMessage import FlashMessage
flash = FlashMessage()
def fetch_all(command, parser, current_db, table_list):
    """
    This function is responsible to fetch data, like select * from table_name.

    @param command: This is the a command
    @param parser: This is the parser
    @param current_db: This is the current database
    @param table_list: This is the table list
    
    """
    
    if current_db:
        table_name = parser.get_arg(3)
        if table_name:
            table_list.select_all(table_name)
        else:
            flash.error_message(
                "No table name provided for 'select all' command.",
                "No table name provided for 'select all' command.",
            )
    else:
        flash.error_message(
            "No database selected when attempting to select all data.",
            "No database selected when attempting to select all data.",
        )
