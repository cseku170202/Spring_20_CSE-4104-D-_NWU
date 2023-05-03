
import tkinter as tk
import re
from prettytable import PrettyTable

KEYWORDS = r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long' \
           r'|register|return|short|signed|sizeof|static|switch|typedef|union|unsigned|void|volatile|while|string' \
           r'|class|struct|include)\b'
Function = r'\b(printf|main|scanf|malloc|calloc|free|strlen|strcmp|strcpy|strcat|memset|memcpy|cout|cin|new|delete|string|vector|map|sort|find)\b'
IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
OPERATOR = r'(\+\+)|(\+)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)|(\$)|(&)|(!)|(,)|(<)|(>)|(\{)|(})|(\^)|(~)|(\[)|(])'
HEADER = r'(#\s*include\s*)([<"][^"\n<>]*\.(h|hpp|H|hh|HPP|hhp|inc|INC)[>"])'
SPECIAL_CHAR = r'[;@#\'\'?:".|=(){}\[\]\\]+'
NUMERAL = r'[0-9]+'
STRING_LITERAL = r'"([^"\\]|\\.|\\\\)*"'


def extract_tokens(code: str) -> list:
    keyword_regex = re.compile(KEYWORDS)
    function_regex = re.compile(Function)
    identifier_regex = re.compile(IDENTIFIER)
    operator_regex = re.compile(OPERATOR)
    special_character_regex = re.compile(SPECIAL_CHAR)
    numeral_regex = re.compile(NUMERAL)
    header_regex = re.compile(HEADER)
    string_literal_regex = re.compile(STRING_LITERAL)
    comment_regex = re.compile('//.*?$')
    empty_line_regex = re.compile('^\s*$')

    tokens = []
    lines = code.split('\n')
    line_num = 1
    string_literals = []

    for line in lines:
        line = line.strip()
        if not line or comment_regex.match(line) or empty_line_regex.match(line):
            line_num += 1
            continue


        line_tokens = []
        words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|<\w+\.h>|[;@#?.|=(){}]+|\S', line)

        for word in words:
            if keyword_regex.match(word):
                line_tokens.append((word, 'Keyword', line_num))
            elif function_regex.match(word):
                line_tokens.append((word, 'Function', line_num))
            elif identifier_regex.match(word):
                line_tokens.append((word, 'Identifier', line_num))
            elif operator_regex.match(word):
                line_tokens.append((word, 'Operator', line_num))
            elif special_character_regex.match(word):
                line_tokens.append((word, 'Special Character', line_num))
            elif numeral_regex.match(word):
                line_tokens.append((word, 'Numeral', line_num))
            elif match := header_regex.match(word):
                tokens.append((match.group(2), 'Header', line_num))
            elif string_literal_regex.match(word):
                line_tokens.append((word, 'String Literal', line_num))
                string_literals.append(word)

        tokens.extend(line_tokens)
        line_num += 1

    # show all string literals as a single string
    print("String Literals: ", " ".join(string_literals))



    return tokens



def display_tokens():
    try:
        # get the code from the input field
        code = code_input.get('1.0', tk.END)

        # check if code input is empty
        if not code.strip():
            token_display.insert(tk.END, "Please enter some code to extract tokens.\n")
            return

        # extract the tokens from the code
        tokens = extract_tokens(code)

        # clear the output field
        token_display.delete('1.0', tk.END)

        # create a pretty table instance
        table = PrettyTable()

        # set the field names and alignment
        table.field_names = ['Token', 'Keyword', 'Line Number']
        table.align['Token'] = 'c'
        table.align['Keyword'] = 'c'
        table.align['Line Number'] = 'c'

        # add rows to the table
        for token in tokens:
            table.add_row([token[0], token[1], token[2]])

        # display the table in a tkinter widget
        table_string = table.get_string()
        token_display.insert(tk.END, table_string)

        # configure the tag for centering
        token_display.tag_configure('center', justify='center')

        # center the table
        token_display.tag_add('center', '1.0', 'end')

        # adjust font size
        token_display.configure(font=("Courier", 10))

    except tk.TclError as e:
        # handle any errors related to Tkinter widgets
        print(f"Tkinter error: {str(e)}")
    except Exception as e:
        # handle any other exceptions
        print(f"Error: {str(e)}")


window = tk.Tk()
window.configure(bg='#dedada')
window.title('Lexical Analyzer')

# create a label for the input field
input_label = tk.Label(window, width=57, font=('Arial', 9), text="Enter your code:")
input_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

# create a Text widget for input
code_input = tk.Text(window, font=('Courier', 10), height=15, width=50, bg='#e8dada', fg='black')
code_input.grid(row=1, column=0, padx=10, pady=10)

# create a label for the output field
output_label = tk.Label(window, width=57, font=('Arial', 9), text="Tokenization")
output_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

# create a Text widget for output
token_display = tk.Text(window, font=('Courier', 10), height=15, width=50, bg='#e8dada', fg='black')
token_display.grid(row=1, column=1, padx=10, pady=10)

# create a scrollbar for the output Text widget
scrollbar = tk.Scrollbar(window, command=token_display.yview)
scrollbar.grid(row=1, column=2, sticky='ns')

# attach the scrollbar to the output Text widget
token_display.config(yscrollcommand=scrollbar.set)


# create a function to clear input and output widgets
def clear_widgets():
    code_input.delete('1.0', 'end')
    token_display.delete('1.0', 'end')


# create a button to extract tokens
extract_button = tk.Button(window, text="Extract Tokens", font=('Arial', 10), bg='#cfe2f3', fg='black',
                           command=lambda: display_tokens())
extract_button.grid(row=2, column=0, padx=25, pady=25)

# create a button to clear input and output widgets
clear_button = tk.Button(window, text="Clear", font=('Arial', 10), bg='#f4cccc', fg='black', command=clear_widgets,
                         width=7)
clear_button.grid(row=2, column=0, padx=25, pady=25, columnspan=2)


def show_symbol_table():
    global symbol_display

    # create a new window for the symbol table
    symbol_window = tk.Toplevel(window)
    symbol_window.configure(bg='#bacbda')
    symbol_window.title('Symbol Table')

    # add a label and text widget to the symbol window
    symbol_label = tk.Label(symbol_window, width=57, font=('Arial', 9), text="Symbol Table:")
    symbol_label.pack(padx=10, pady=10)

    symbol_display = tk.Text(symbol_window, font=('Courier', 10), height=15, width=50, bg='#e8dada', fg='black')
    symbol_display.pack(padx=10, pady=10)

    # change the background color of symbol_display
    symbol_display.configure(bg='#dedada')

    # extract the tokens from the code in the input field
    code = code_input.get('1.0', tk.END)
    tokens = extract_tokens(code)

    # create symbol table
    sym_table = {}
    for token in tokens:
        if token[1] == 'Identifier':
            sym_table[token[0]] = ['N/A', 'N/A']

    # update symbol table with data type and value
    for i, token in enumerate(tokens):
        if token[1] == 'Identifier':
            if i > 0 and tokens[i - 1][1] in ('Data_Type', 'Header') and tokens[i - 1][0] not in (
                    'if', 'while', 'for'):
                sym_table[token[0]][0] = tokens[i - 1][0]  # data type
            elif i > 0 and tokens[i - 1][1] == 'Operator' and tokens[i - 1][0] == '=':
                sym_table[token[0]][1] = tokens[i + 1][0]  # value

    # create a pretty table instance
    table = PrettyTable()

    # set the field names and alignment
    table.field_names = ['Identifier', 'Data_Type', 'Value']
    table.align['Identifier'] = 'c'
    table.align['Data_Type'] = 'c'
    table.align['Value'] = 'c'

    # add rows to the table
    for identifier, data in sym_table.items():
        table.add_row([identifier, data[0], data[1]])

    # display the table in the symbol_display Text widget
    table_string = table.get_string()
    symbol_display.insert(tk.END, table_string)

    # configure the tag for centering
    symbol_display.tag_configure('center', justify='center')

    # center the table
    symbol_display.tag_add('center', '1.0', 'end')

    # adjust font size
    symbol_display.configure(font=("Courier", 10))


# define symbol_display as a global variable
symbol_display: None = None

# create a button to show the symbol table
symbol_button = tk.Button(window, text="Symbol Table", font=('Arial', 10), bg='#d9d2e9', fg='black',
                          command=show_symbol_table)
symbol_button.grid(row=2, column=1, padx=25, pady=25)

# run the tkinter event loop
window.mainloop()
