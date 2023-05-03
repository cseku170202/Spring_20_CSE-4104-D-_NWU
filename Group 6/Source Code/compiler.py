from tkinter import*
import tokenize
from io import BytesIO
import tkinter as tk
import os

def extract_tokens(code):
    tokens = []
    for tok in tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
        # if tok.type == tokenize.OP:
        #     tokens.append((tok.string, 'Operator', tok.start[0]))
        if tok.string in ['+', '-', '*', '/', '%']:
            tokens.append((tok.string, 'Arithmetic OP', tok.start[0]))
        elif tok.string in ['==', '!=', '>', '<', '%']:
            tokens.append((tok.string, 'Relational OP', tok.start[0]))
        elif tok.string in ['=', '+=', '-=']:
            tokens.append((tok.string, 'Assignment OP', tok.start[0]))
        elif tok.string in ['(', ')', '{', '}', '[', ']']:
            tokens.append((tok.string, 'Bracket', tok.start[0]))
        elif tok.string in [',', ';', ':', '#', '@', '"']:
            tokens.append((tok.string, 'Punctuator', tok.start[0]))
        elif tok.type == tokenize.NUMBER:
            tokens.append((tok.string, 'Numeral', tok.start[0]))
        elif tok.type == tokenize.NAME:
            if tok.string in ['if', 'else', 'return', 'int', 'for', 'switch', 'case', 'while', 'do', 'float', 'double',
                              'string', 'char']:
                tokens.append((tok.string, 'Keyword', tok.start[0]))
            else:
                tokens.append((tok.string, 'Identifier', tok.start[0]))
    return tokens

def display_tokens():
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

def generate(code):
    tokens = []
    for tok in tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
        if tok.type == tokenize.NUMBER:
            print((tok.string, tok.type, tok.start[0]))
        elif tok.string in ['for', 'while', 'do']:
            print((tok.string, 'Loop', tok.start[0]))
        elif tok.string in ['if', 'else', 'elseif', 'elif']:
            print((tok.string, 'Condition', tok.start[0]))
        elif tok.string in ['int', 'float', 'double', 'char', 'bool']:
            print((tok.string, 'datatype', tok.start[0]))
        elif tok.type == tokenize.NAME:
            if tok.string in ['if', 'else', 'return', 'for', 'switch', 'case', 'while', 'do', 'string', 'scanf', 'input', 'cin', 'printf', 'print', 'cout']:
                print((tok.string, 'Keyword', tok.start[0]))
            else:
                tokens.append((tok.string, '50', tok.start[0]))
    return tokens

def generateTable():
    code = code_input.get("1.0", "end-1c")  # get code from input field
    tokens = generate(code)  # extract tokens from code

    # clear previous token display
    token_display.delete("1.0", tk.END)

    # display tokens, keywords, and line numbers in a single line at the top of the output window
    token_display.insert(tk.END, f"{'Token':<15} {'Value':<15}\n")
    token_display.insert(tk.END, f"{'-' * 15:<15} {'-' * 15:<15}\n")
    for tok in tokens:
        token_display.insert(tk.END, f"{tok[0]:<15} {tok[1]:<15}\n")

    # set background color of input and output panes

# create popup window
popup = tk.Tk()
popup.geometry("1050x500")

popup.title("Token Extractor")
popup.configure(bg='#23262b')
yscroll=Scrollbar(popup)
yscroll.pack(side=RIGHT,fill=Y)
textrea=Text(popup,yscrollcommand=yscroll.set)

yscroll.config(command=textrea.yview)
textrea.config(yscrollcommand=yscroll.set)

# create paned window to divide window into two panes
paned_window = tk.PanedWindow(popup, orient=tk.HORIZONTAL)
paned_window.pack(expand=True, fill=tk.X)
paned_window.configure(bg='#23262b')

# create input field for code
code_input = tk.Text(paned_window, height=10)
paned_window.add(code_input)
code_input.configure(bg='#EBF5FB')

# create text widget to display tokens
token_display = tk.Text(paned_window)
paned_window.add(token_display)
token_display.configure(bg='#EBF5FB')

# create button to extract tokens
extract_button = tk.Button(popup, text="Compile", font=('Tahoma',15), fg='#ffffff', bg='#1675f2', command=lambda:display_tokens().place(x=100,y=2000))
extract_button.pack(pady=15)
symbolTable = tk.Button(popup, text="Generate", font=('Tahoma',15), fg='#ffffff', bg='#1675f2',command=lambda:generateTable().place(x=200,y=2000))
symbolTable.pack()
popup.mainloop()