from FlashMessage import FlashMessage

flash = FlashMessage()
def custom_command(command, table_list):
    """Handle custom syntax like 'table::all()' or 'table::all(<limit>)'."""
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
