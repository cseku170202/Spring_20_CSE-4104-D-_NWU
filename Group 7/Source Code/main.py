import tkinter as tk

from tkinter import*
from tkinter import ttk


# Define a list of keywords
keywords = ["if", "else", "while", "for", "return","include","int","float"]

# Define a list of operators
operators = ["+", "-", "*", "/", "=", "==", "<", ">", "<=", ">=","#"]

# Define a list of delimiters
delimiters = ["(", ")", "{", "}", ",", ";"]
# Define a header file
header_file=["stdio.h"]
# Define Built in function
Function= ["main", "printf", "scanf"]

# Define a function to perform lexical analysis on a line of code
def analyze_line(line):
    tokens = []
    current_token = ""

    # Loop through each character in the line
    for char in line:
        # If the character is a whitespace or delimiter, add the current token to the list of tokens
        if char.isspace() or char in delimiters:
            if current_token:
                tokens.append(current_token)
                current_token = ""

            # If the character is a delimiter, add it to the list of tokens
            if char in delimiters:
                tokens.append(char)
        # If the character is an operator, add the current token to the list of tokens and add the operator as a separate token
        elif char in operators:
            if current_token:
                tokens.append(current_token)
                current_token = ""

            tokens.append(char)
        # If the character is none of the above, add it to the current token
        else:
            current_token += char

    # Add the last token to the list of tokens if there is one
    if current_token:
        tokens.append(current_token)

    # Classify each token as a keyword, operator, identifier, or literal
    classified_tokens = []
    for token in tokens:
        if token in keywords:
            classified_tokens.append((token, "Keyword"))
        elif token in operators:
            classified_tokens.append((token, "Operator"))
        elif token in delimiters:
            classified_tokens.append((token, "Delimiter"))
        elif token in header_file:
            classified_tokens.append((token, "header_file"))
        elif token in Function:
            classified_tokens.append((token, "function"))

        elif token.isdigit():
            classified_tokens.append((token, "Literal"))
        else:
            classified_tokens.append((token, "Identifier"))

    return classified_tokens

# Define a function to perform lexical analysis on the input text
def analyze_text():
    # Clear the output text box
    output_text.delete("1.0", "end")

    # Get the input text
    input_str = input_text.get("1.0", "end")

    # Split the input text into lines and analyze each line
    lines = input_str.split("\n")
    for i, line in enumerate(lines):
        # Perform lexical analysis on the line
        tokens = analyze_line(line)

        # Add the tokens to the output text box
        for token in tokens:
            output_text.insert("end", f"{token[0]:<10} {token[1]:<10} Line {i+1}\n")


def table():
    line =tk.text("1.0", "end-1c")  # get code from input field
    tokens = list(analyze_line(line))  # convert iterator to list

    symbol_table = {}  # initialize symbol table dictionary

    # loop through tokens to populate symbol table
    for i, tok in enumerate(tokens):
        if tok[1] == 'IdentifierDeclaration':
            # get the data type and value of the identifier
            if i < len(tokens) - 2 and tokens[i+1][0] == '=':
                value = tokens[i+2][0]  # access element using subscript notation
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
    symbol_window = Toplevel(root)
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
        data_type = data['Data Type'] if data['Data Type'] else '-'
        value = data['Value'] if data['Value'] is not None else '-'
        table.insert(parent='', index='end', iid=identifier, text=identifier, values=(data_type, value))



# Create the main window
root = tk.Tk()
root.title("Lexical Analyzer")

# Create the input text box

input_text = tk.Text(root, height=20,background="Yellow", width=70)
input_text.pack(side=tk.LEFT, padx=10, pady=10)
C_button = tk.Button(root, text="Show Symbol Table",font="times 15 bold", bg="Red", command=table)
C_button.pack(side=tk.BOTTOM, padx=10,pady=10)

# Create the output text box
output_text = tk.Text(root, height=20,background="Gray", width=70)
output_text.pack(side=tk.RIGHT, padx=10, pady=10)

# Create the analyze button
analyze_button = tk.Button(root, text="Analyze",font="times 15 bold", bg="green", command=analyze_text)
analyze_button.pack(side=tk.BOTTOM, pady=150)

# Start the main event loop
root.mainloop()
