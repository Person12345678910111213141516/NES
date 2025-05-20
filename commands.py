from editor import (
    handle_insert_above, handle_open_file, handle_save_as,
    handle_find_text, handle_terminal_mode, handle_colours_menu
)

import sys

help_messages = {
    '': [
        "Type a command name to get help with it.",
        "Commands: getHelp, setCursor, openFile, saveAs, findText, coloursMenu, closeEditor, insertAbove, terminalMode"
    ],
    'getHelp': [
        "getHelp command",
        "Gives help with commands",
        "Arguments: None -- Bring up the generic help menu, Any Command -- Bring up the help menu for a command"
    ],
    'setCursor': [
        "setCursor command",
        "Changes the line number",
        "Arguments: Any Number -- Go to line number"
    ],
    'openFile': [
        "openFile command",
        "opens a file to edit",
        "Arguments: file name -- file to open"
    ],
    'saveAs': [
        "saveAs command",
        "saves a file",
        "Arguments: file name -- name to save as"
    ],
    'findText': [
        "findText command",
        "find text and return the line number it occurs on",
        "Arguments: RegEx or string -- characters to look for"
    ],
    'coloursMenu': [
        "coloursMenu command",
        "change text editor colours",
        "Arguments: None -- Colours will be set in the menu"
    ],
    'closeEditor': [
        "closeEditor command",
        "closes the text editor",
        "Arguments: None -- arguments not required"
    ],
    'insertAbove': [
        "insertAbove command",
        "inserts a new line above the line given",
        "Arguments: Any Number -- Go line number to insert above"
    ],
    'terminalMode': [
        "terminalMode command",
        "run bash code in the editor",
        "Arguments: command to run"
    ],
}

def show_help(state, arg):
    state.linen -= 1
    if arg in help_messages:
        for msg in help_messages[arg]:
            print(f"{state.title2}{msg}")
    else:
        print(f"{state.title1}{help_messages[''][0]}")
        print(help_messages[''][1])

def handle_close_editor():
    sys.exit(0)

def handle_input(state, data):
    command, arg = '', ''
    parts = data.split(" ", 1)
    command = parts[0]
    if len(parts) > 1:
        arg = parts[1]
    if command == 'getHelp':
        show_help(state, arg)
    elif command == 'openFile':
        handle_open_file(state, arg)
        state.current_filename = arg  # <-- Set the filename for syntax highlighting
    elif command == 'setCursor':
        if arg.isdecimal():
            state.linen = max(0, int(arg))
    elif command == 'saveAs':
        handle_save_as(state, arg)
    elif command == 'findText':
        handle_find_text(state, arg)
    elif command == 'coloursMenu':
        handle_colours_menu(state)
        return
    elif command == 'terminalMode':
        handle_terminal_mode(state, arg)
    elif command == 'insertAbove':
        handle_insert_above(state, arg)
    elif command == 'closeEditor':
        handle_close_editor()
    elif command == '+':
        handle_save_as(state, "file.txt")
    else:
        if state.write_flag:
            state.input_lines[state.linen] = data[:1023]
            state.linen += 1
    return True