from tkinter import*
import tokenize
from io import BytesIO
import tkinter as tk
import os
from tkinter import ttk

def table():
    code =code_input.get("1.0", "end-1c")  # get code from input field
    tokens = list(extract_tokens(code))  # convert iterator to list

    symbol_table = {}  # initialize symbol table dictionary

    # loop through tokens to populate symbol table
    for i, tok in enumerate(tokens):
        if tok[1] == 'IdentifierDeclaration':
            # get the data type and value of the identifier
            if i < len(tokens) - 2 and tokens[i + 1][0] == '=':
                value = tokens[i + 2][0]  # access element using subscript notation
                try:
                    value = int(value)
                    symbol_table[tok[0]] = {'Data Type': 'int', 'Value': value}
                except ValueError:
                    try:
                        value = float(value)
                        symbol_table[tok[0]] = {'Data Type': 'float', 'Value': value}
                    except ValueError:
                        symbol_table[tok[0]] = {'Data Type': 'string', 'Value': value}
            else:
                symbol_table[tok[0]] = {'Data Type': None, 'Value': None}
        elif tok[1] == 'Identifier' and tok[0] not in symbol_table:
            symbol_table[tok[0]] = {'Data Type': None, 'Value': None}

    # loop through tokens again to update symbol table with data type and value
    for i, tok in enumerate(tokens):
        if tok[1] == 'Identifier' and tok[0] in symbol_table:
            # check if the data type and value have already been set
            if symbol_table[tok[0]]['Data Type'] is None:
                # check if the identifier is being assigned a value
                if i < len(tokens) - 2 and tokens[i + 1][0] == '=':
                    value = tokens[i + 2][0]  # access element using subscript notation
                    try:
                        value = int(value)
                        symbol_table[tok[0]]['Data Type'] = 'int'
                        symbol_table[tok[0]]['Value'] = value
                    except ValueError:
                        try:
                            value = float(value)
                            symbol_table[tok[0]]['Data Type'] = 'float'
                            symbol_table[tok[0]]['Value'] = value
                        except ValueError:
                            symbol_table[tok[0]]['Data Type'] = 'string'
                            symbol_table[tok[0]]['Value'] = value
            elif tok[1] == 'IdentifierDeclaration' and tokens[i + 1][0] == '=':
                value = tokens[i + 2][0]  # access element using subscript notation
                try:
                    value = int(value)
                    symbol_table[tok[0]]['Data Type'] = 'int'
                    symbol_table[tok[0]]['Value'] = value
                except ValueError:
                    try:
                        value = float(value)
                        symbol_table[tok[0]]['Data Type'] = 'float'
                        symbol_table[tok[0]]['Value'] = value
                    except ValueError:
                        symbol_table[tok[0]]['Data Type'] = 'string'
                        symbol_table[tok[0]]['Value'] = value

    # create a new window to display the symbol table
    symbol_window = Toplevel(popup)
    symbol_window.title("Symbol Table")
    symbol_window.configure(background="#b9ede2")

    # set dimensions and position of the new window
    window_width, window_height = 500, 400
    screen_width = symbol_window.winfo_screenwidth()
    screen_height = symbol_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    symbol_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # create a table to display the symbol table
    table_frame = tk.Frame(symbol_window)
    table_frame.pack(fill=tk.BOTH, expand=True)
    table = ttk.Treeview(table_frame)
    table.pack(fill=tk.BOTH, expand=True)

    # configure the columns of the table
    table['columns'] = ('Data Type', 'Value')

    # set column headings
    table.heading('#0', text='Identifier')
    table.heading('Data Type', text='Data Type')
    table.heading('Value', text='Value')

    # set column widths
    table.column('#0', width=150)
    table.column('Data Type', width=150)
    table.column('Value', width=150)

    # populate the table with data from the symbol table dictionary
    for identifier, data in symbol_table.items():
        data_type = data['Data Type'] if data['Data Type'] else 'Number'
        value = data['Value'] if data['Value'] is not None else '-'
        table.insert(parent='', index='end', iid=identifier, text=identifier, values=(data_type, value))


def extract_tokens(code):
    tokens = []
    variables = set()  # initialize set to keep track of variables
    declared = set()  # initialize set to keep track of declared variables

    # parse the code and extract the tokens
    for tok in tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
        if tok.type == tokenize.OP:
            if tok.string in ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!', '&', '|',
                              '^', '~', '<<', '>>']:
                tokens.append((tok.string, 'Operator', tok.start[0]))


            else:
                tokens.append((tok.string, 'Symbol', tok.start[0]))
        elif tok.type == 63:
            tokens.append(('#', 'Symbol', tok.start[0]))
        elif tok.type == tokenize.NAME and not tok.string.startswith('"') and not tok.string.startswith("'"):
            if tok.string in ['if', 'else', 'return', 'int', 'for', 'switch', 'case', 'while', 'do', 'float', 'double',
                              'string', 'char', 'include', 'stdio']:
                tokens.append((tok.string, 'Keyword', tok.start[0]))
            else:
                if tok.string in declared:
                    tokens.append((tok.string, 'Identifier', tok.start[0]))
                else:
                    tokens.append((tok.string, 'Identifier', tok.start[0]))
        elif tok.type == tokenize.STRING:
            tokens.append((tok.string, 'String', tok.start[0]))

        # check if the variable is being declared
        if tok.type == tokenize.NAME and not tok.string.startswith('"') and not tok.string.startswith("'") and \
                tokens[-1][0] not in ['int', 'float', 'double', 'char', 'string'] and \
                tokens[-1][1] != 'Symbol' and tokens[-1][0] != '(' and \
                tokens[-1][0] not in ['.', '('] and \
                tokens[-1][0] not in declared:
            declared.add(tokens[-1][0])
    return tokens


def display_tokens(input_bg, output_bg):
    code = code_input.get("1.0", "end-1c")  # get code from input field
    tokens = extract_tokens(code)  # extract tokens from code

    # clear previous token display
    token_display.delete("1.0", tk.END)

    # display tokens, keywords, and line numbers in a single line at the top of the output window
    token_display.insert(tk.END, f"{'Token':<15} {'Keyword':<15} {'Line Number':<15}\n")
    token_display.insert(tk.END, f"{'-' * 15:<15} {'-' * 15:<15} {'-' * 15:<15}\n")
    for tok in tokens:
        token_display.insert(tk.END, f"{tok[0]:<15} {tok[1]:<15} {tok[2]:<15}\n")

    # set background color of input and output panes
    code_input.configure(background=input_bg)
    token_display.configure(background=output_bg)



# create popup window
popup = tk.Tk()
popup.geometry("1050x500")

popup.title("Token Extractor")
popup.configure(bg='#856ff8')
yscroll=Scrollbar(popup)
yscroll.pack(side=RIGHT,fill=Y)
textrea=Text(popup,yscrollcommand=yscroll.set)

yscroll.config(command=textrea.yview)
textrea.config(yscrollcommand=yscroll.set)

# create paned window to divide window into two panes
paned_window = tk.PanedWindow(popup, orient=tk.HORIZONTAL)
paned_window.pack(expand=True, fill=tk.X)
paned_window.configure(bg='#EBF5FB')


# create input field for code
code_input = tk.Text(paned_window, height=10)
paned_window.add(code_input)
code_input.configure(bg='#EBF5FB')

# create text widget to display tokens
token_display = tk.Text(paned_window)
paned_window.add(token_display)
token_display.configure(bg='#EBF5FB')

# create button to extract tokens
extract_button = tk.Button(popup, text="Extract",height=1, width=10, bg='pink',command=lambda:display_tokens('#add8e6', '#add8e6'),font=("Times New Roman", 15, "bold"))
extract_button.pack()
btn2 = Button(popup, text="Symbol Table",command=table, height=1, width=10, bg="pink", font=("Times New Roman", 15, "bold"))
btn2.pack()





popup.mainloop()
