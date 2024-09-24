from FlashMessage import FlashMessage
flash = FlashMessage()
def switch_database(db_list, parser):
    """
    Switches to a different database.

    Args:
        db_list (DatabaseList): An instance of DatabaseList.
        parser (CommandParser): An instance of CommandParser.

    Returns:
        str: The name of the database to switch to.

    Raises:
        mysql.connector.Error: If the database does not exist.
    """

    db_name = parser.get_arg()
    if db_list.check_database(db_name):
        db_list.select_database(db_name)
        return db_name
    else:
        flash.error_message(
            f"ERROR 1049 (42000): Unknown database... '{db_name}' ",
            f"{db_name} does not exist",
        )