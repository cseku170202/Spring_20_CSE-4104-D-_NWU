import re
import nltk
from tkinter import*
import tkinter as tk
import tokenize
from io import BytesIO
from tkinter import ttk
from prettytable import PrettyTable

import sys


root = Tk()
root.title("Lexical Analyzer")
root.configure(background="#b9ede2")
window_width,window_height=1300,630

screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()

position_top=int(screen_height/2-window_height/2)
position_right=int(screen_width/2-window_width/2)

root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

label1 = Label(root, text="Enter Sample code Here", font=("Times New Roman", 15, "bold"),background="#b9ede2", padx=20, pady=20)
label1.grid(row=0, column=2,padx=(150,0))


label2 = Label(root, text="Token \n ", font=("Times New Roman", 15, "bold"),background="#b9ede2", padx=20, pady=20)
label2.grid(row=0, column=4,padx=(300,0))

entry = Text(root,font=("Times New Roman", 10, "bold"), bg="#c7ccc6",  width=40, borderwidth=5)
entry.grid(row=1, column=2,pady=3, columnspan=2, padx=(70,0))


def extract_tokens(code):
    tokens = []
    variables = set()  # initialize set to keep track of variables
    declared = set()   # initialize set to keep track of declared variables

    # parse the code and extract the tokens
    for tok in tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
        if tok.type == tokenize.OP:
            if tok.string in ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!', '&', '|',
                              '^', '~', '<<', '>>']:
                tokens.append((tok.string, 'Operator', tok.start[0]))
            else:
                tokens.append((tok.string, 'Symbol', tok.start[0]))
        elif tok.type == tokenize.NAME and not tok.string.startswith('"') and not tok.string.startswith("'"):
            if tok.string in ['if', 'else', 'return', 'int', 'for', 'switch', 'case', 'while', 'do', 'float', 'double',
                              'string', 'char']:
                tokens.append((tok.string, 'Keyword', tok.start[0]))
            else:
                if tok.string in declared:
                    tokens.append((tok.string, 'Identifier', tok.start[0]))
                else:
                    tokens.append((tok.string, 'Function', tok.start[0]))
        elif tok.type == tokenize.STRING:
            tokens.append((tok.string, 'String', tok.start[0]))

        # check if the variable is being declared
        if tok.type == tokenize.NAME and not tok.string.startswith('"') and not tok.string.startswith("'") and \
                tokens[-1][0] not in ['int', 'float', 'double', 'char', 'string'] and \
                tokens[-1][1] != 'Symbol' and tokens[-1][0] != '(' and \
                tokens[-2][0] not in ['.', '('] and \
                tokens[-1][0] not in declared:
            declared.add(tokens[-1][0])

    # loop through list of undeclared identifiers to determine their data types
    for i, tok in enumerate(tokens):
        if tok[1] == 'Function':
            # look for an equals sign after the identifier
            if i < len(tokens) - 2 and tokens[i + 1][0] == '=':
                value = tokens[i + 2][0]  # access element using subscript notation
                try:
                    value = int(value)
                    tokens[i] = (value, 'Number', tok[2])
                    declared.add(tok[0])
                except ValueError:
                    try:
                        value = float(value)
                        tokens[i] = (value, 'Number', tok[2])
                        declared.add(tok[0])
                    except ValueError:
                        tokens[i] = (value, 'String', tok[2])
                        declared.add(tok[0])

    return tokens


def display_tokens():
    # code = entry.get("1.0", "end-1c")  # get code from input field
    # tokens = extract_tokens(code)  # extract tokens from code
    #
    # # clear previous token display
    # entry1.delete("1.0", tk.END)
    #
    # # display tokens, keywords, and line numbers in a single line at the top of the output window
    # entry1.insert(tk.END, f"{'Token':<15} {'Keyword':<15} {'Line Number':<15}\n")
    # entry1.insert(tk.END, f"{'-' * 15:<15} {'-' * 15:<15} {'-' * 15:<15}\n")
    # for tok in tokens:
    #     entry1.insert(tk.END, f"{tok[0]:<15} {tok[1]:<15} {tok[2]:<15}\n")


    try:
        # get the code from the input field
        code = entry.get("1.0", "end-1c")

        # check if code input is empty
        if not code.strip():
            entry1.insert(tk.END, "Please enter some code to extract tokens.\n")
            return

        # extract the tokens from the code
        tokens = extract_tokens(code)

        # clear the output field
        entry1.delete('1.0', tk.END)

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
        entry1.insert(tk.END, table_string)

        # configure the tag for centering
        entry1.tag_configure('center', justify='center')

        # center the table
        entry1.tag_add('center', '1.0', 'end')

        # adjust font size
        entry1.configure(font=("Courier", 10))

    except tk.TclError as e:
        # handle any errors related to Tkinter widgets
        print(f"Tkinter error: {str(e)}")
    except Exception as e:
        # handle any other exceptions
        print(f"Error: {str(e)}")





def table():
    global symbol_display

    # create a new window for the symbol table
    symbol_window = tk.Toplevel(root)
    symbol_window.configure(bg='#b9ede2')
    symbol_window.title('Symbol Table')

    # add a label and text widget to the symbol window
    symbol_label = tk.Label(symbol_window, width=57, font=('Arial', 9), text="Symbol Table:")
    symbol_label.pack(padx=10, pady=10)

    symbol_display = tk.Text(symbol_window, font=('Courier', 10), height=15, width=50, bg='#e8dada', fg='black')
    symbol_display.pack(padx=10, pady=10)

    # change the background color of symbol_display
    symbol_display.configure(bg='#dedada')

    # extract the tokens from the code in the input field
    code = entry.get("1.0", "end-1c")
    tokens = extract_tokens(code)

    # create symbol table
    sym_table = {}
    for token in tokens:
        if token[1] == 'Identifier':
            sym_table[token[0]] = ['N/A', 'N/A']

    # update symbol table with data type and value
    for i, token in enumerate(tokens):
        if token[1] == 'Identifier':
            if i > 0 and tokens[i - 1][1] in ('Keyword', 'Header') and tokens[i - 1][0] not in (
                    'if', 'while', 'for'):
                sym_table[token[0]][0] = tokens[i - 1][0]  # data type
            elif i > 0 and tokens[i - 1][1] == 'Operator' and tokens[i - 1][0] == '=':
                sym_table[token[0]][1] = tokens[i + 1][0]  # value

    # create a pretty table instance
    table = PrettyTable()

    # set the field names and alignment
    table.field_names = ['Identifier', 'Data Type', 'Value']
    table.align['Identifier'] = 'c'
    table.align['Data Type'] = 'c'
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




# create text widget to display tokens
# token_display = tk.Text(root)
# root.add(token_display)
# token_display.configure(bg='#EBF5FB')


entry1 = Text(root,font=("Times New Roman", 10, "bold"), bg="#c7ccc6",  width=80, borderwidth=5)
entry1.grid(row=1, column=4, padx=(200,0))


btn1 = Button(root, text="Analyze",command=display_tokens, height=1, width=7, bg="#c9c695", font=("Times New Roman", 15, "bold"), relief=RIDGE, bd=9, highlightthickness=2, highlightbackground="#5e8c57")
btn1.grid(row=2, columnspan=2, column=2, ipadx=30, pady=40, padx=(50,0))

btn2 = Button(root, text="Symbol Table",command=table, height=1, width=10, bg="#c9c695", font=("Times New Roman", 15, "bold"), relief=RIDGE, bd=9, highlightthickness=2, highlightbackground="#5e8c57")
btn2.grid(row=2, columnspan=2, column=4, ipadx=30, pady=40, padx=(300,0))


root.mainloop()