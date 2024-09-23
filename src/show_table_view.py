from FlashMessage import FlashMessage

flash = FlashMessage()


def get_table_view(command, parser, current_db, table_list):
    """Handle the 'desc' command to describe a table."""
    if current_db:
        table_name = parser.get_arg()
        table_list.show_create_tables(table_name)
    else:
        flash.error_message("ERROR 1046 (3D000): No database selected")
