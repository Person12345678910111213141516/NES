import re
import sys
import subprocess
import shutil
from colors import Colours, lookup_fg

MAX_LINES = 1000
MAX_LINE_LENGTH = 1024

class EditorState:
    def __init__(self):
        self.input_lines = [''] * MAX_LINES
        self.linen = 0
        self.write_flag = True
        self.title1 = None
        self.title2 = None
        self.nums = None
        self.other = None
        self.colours = Colours()

def get_display_lines():
    try:
        height = shutil.get_terminal_size().lines
        return max(1, height - 3)
    except Exception:
        return 20

def highlight_python(line, state):
    # Highlight numbers and booleans (Title1), strings (Title2), keywords (Number), rest (Other)
    # Order: strings, numbers, booleans, keywords, rest
    # We'll use regex to find tokens and replace them with colored versions

    # Python keywords (excluding True/False/None)
    keywords = r'\b(?:def|class|import|from|if|else|elif|for|while|return|try|except|with|as|pass|break|continue|in|is|not|and|or|print|lambda|yield|global|nonlocal|assert|del)\b'
    # Booleans and None
    bools = r'\b(?:True|False|None)\b'
    # Numbers (int, float, scientific)
    numbers = r'\b\d+(\.\d+)?([eE][+-]?\d+)?\b'
    # Strings (single, double, triple)
    strings = r'(\'\'\'(?:.|\n)*?\'\'\'|"""(?:.|\n)*?"""|\'[^\']*\'|"[^"]*")'

    # Highlight strings first
    def string_repl(m):
        return f"{state.title2}{m.group(0)}{state.colours.reset}"

    line = re.sub(strings, string_repl, line)

    # Highlight numbers
    def number_repl(m):
        return f"{state.title1}{m.group(0)}{state.colours.reset}"

    line = re.sub(numbers, number_repl, line)

    # Highlight booleans/None
    def bool_repl(m):
        return f"{state.title1}{m.group(0)}{state.colours.reset}"

    line = re.sub(bools, bool_repl, line)

    # Highlight keywords
    def keyword_repl(m):
        return f"{state.nums}{m.group(0)}{state.colours.reset}"

    line = re.sub(keywords, keyword_repl, line)

    # Optionally, you can color the rest of the line with 'other' (not recommended for readability)
    # But to meet your requirement, wrap the whole line in 'other' and then re-apply the above highlights
    # Instead, we leave non-highlighted text as is, so only the specified tokens are colored

    return line

def handle_insert_above(state, arg):
    line_number = int(arg) - 1
    if 0 < line_number < MAX_LINES:
        for i in range(state.linen, line_number, -1):
            state.input_lines[i] = state.input_lines[i - 1]
        state.input_lines[line_number] = ''
        state.linen += 1
    else:
        print(f"Invalid line number: {line_number + 1}", file=sys.stderr)

def handle_open_file(state, filename):
    state.linen = 0
    try:
        with open(filename, 'r') as fp:
            for line in fp:
                if state.linen < MAX_LINES:
                    clean_line = line.rstrip('\r\n')
                    state.input_lines[state.linen] = clean_line[:MAX_LINE_LENGTH - 1]
                    state.linen += 1
                else:
                    print("Input limit reached, unable to read more lines.", file=sys.stderr)
                    break
    except IOError as e:
        print(f"Error opening file: {str(e)}", file=sys.stderr)

def handle_save_as(state, filename):
    try:
        with open(filename, 'w') as fp:
            for i in range(MAX_LINES):
                if state.input_lines[i]:
                    fp.write(state.input_lines[i] + "\n")
    except IOError as e:
        print(f"Error saving file: {str(e)}", file=sys.stderr)

def handle_find_text(state, search):
    lines = []
    state.linen -= 1
    pattern = re.compile(search)
    for i, line in enumerate(state.input_lines):
        if line and pattern.search(line):
            lines.append(i)
    print("Matches found at lines:", lines)

def handle_terminal_mode(state, command):
    state.linen -= 1
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        print("\nOutput:\n", output)
    except subprocess.CalledProcessError:
        print("Error executing command.", file=sys.stderr)

def handle_colours_menu(state):
    state.linen -= 1
    col1 = input("Title1? -> ")
    state.title1 = lookup_fg(state.colours, col1.strip())
    col2 = input("Title2? -> ")
    state.title2 = lookup_fg(state.colours, col2.strip())
    col3 = input("Number? -> ")
    state.nums = lookup_fg(state.colours, col3.strip())
    col = input("Others? -> ")
    state.other = lookup_fg(state.colours, col.strip())