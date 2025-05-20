from editor import (
    EditorState,
    get_display_lines,
    highlight_python,
    highlight_c_cpp,
    highlight_java,
    highlight_javascript,
    highlight_csharp,
)
from commands import handle_input

current_filename = None

def get_highlighter(filename):
    if filename is None:
        return None
    ext = filename.lower()
    if ext.endswith('.py'):
        return highlight_python
    elif ext.endswith(('.c', '.cpp', '.h', '.hpp')):
        return highlight_c_cpp
    elif ext.endswith('.java'):
        return highlight_java
    elif ext.endswith(('.js', '.jsx')):
        return highlight_javascript
    elif ext.endswith(('.cs',)):
        return highlight_csharp
    else:
        return None

def iterate(state):
    display_lines = get_display_lines()
    highlighter = get_highlighter(getattr(state, "current_filename", None))
    for i in range(display_lines):
        index = state.linen + i
        if index < 0 or index >= len(state.input_lines):
            print(f"{state.nums}{state.linen + i}{state.colours.reset} {state.other} {state.colours.reset}")
        else:
            if highlighter:
                line = highlighter(state.input_lines[index], state)
            else:
                line = f"{state.other}{state.input_lines[index]}{state.colours.reset}"
            print(f"{state.nums}{state.linen + i}{state.colours.reset} {line}")
    user_input = input(f"\n{state.linen} ")
    if handle_input(state, user_input):
        iterate(state)

if __name__ == "__main__":
    state = EditorState()
    state.title1 = state.colours.fg.blue
    state.title2 = state.colours.fg.yellow
    state.nums = state.colours.fg.green
    state.other = state.colours.fg.red
    state.current_filename = None  # Track the current file for highlighting
    print(f"{state.title1}Terminal Editor{state.colours.reset}")
    print(f"{state.title2}By Stuart Mangione{state.colours.reset}")
    iterate(state)