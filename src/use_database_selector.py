from FlashMessage import FlashMessage
flash = FlashMessage()
def switch_database(db_list, parser):
    """
     This function is responsible to use a database.
        @param db_list: This is the database list
        @param parser: This is the parser
        >>> use databaes_name
         @name 
            Function:
            1. check_database
            2. select_database
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