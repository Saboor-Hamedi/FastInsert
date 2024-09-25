from FlashMessage import FlashMessage

flash = FlashMessage()
def all(command, table_list):
    
    """
    This function is responsible to fetch all data from database\n
    @param command: This is the a command 
    @param table_name: table_name 
    
    All function is able to fetch data with limit
    
    Example:
        >>> table_name::all()  || table_name::all(10)
         
    """
    parts = command.split("::")
    if len(parts) == 2:
        table_name = parts[0].strip()
        action_part = parts[1].strip()
        if action_part == "all" or (
            action_part.startswith("all(") and action_part.endswith(")")
        ):
            limit = None
            if "(" in action_part and action_part.endswith(")"):
                limit_str = action_part[
                    action_part.index("(") + 1 : action_part.index(")")
                ].strip()
                if limit_str.isdigit():
                    limit = int(limit_str)
                elif limit_str:
                    print(f"Invalid limit value: {limit_str}. Please enter an integer.")
                    return
            table_list.all(table_name, limit)
        else:
            flash.error_message(
                f"Invalid action: {action_part}. Use 'table::all()' or 'table::all(<limit>)'."
            )
    else:
        flash.error_message(
            f"Invalid command: {command}. Type '--help' for a list of commands."
        )
