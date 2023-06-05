import tkinter
from tkinter import *
from tkinter import ttk
import re
import nltk

top = tkinter.Tk()
top.geometry("1100x700")
entry1 = tkinter.Text(top, height=20, width=60)
entry1.pack(padx=15, side=LEFT)
output = tkinter.Canvas(top, bg="white", height=400, width=400)
output.pack(padx=15, side=RIGHT)


arrId1 = []
arrId2 = []
arrId3 = []
arrId4 = []
arrVl = []


def lexicalAnalysis():
    input_program_tokens = nltk.wordpunct_tokenize(entry1.get("1.0", "end-1c"))

    RE_Keywords = "auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include"
    RE_Operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"
    RE_Numerals = "^(\d+)$"
    RE_Special_Characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
    RE_Identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    RE_Headers = "([a-zA-Z]+\.[h])"

    # To Categorize The Tokens

    i = 1

    for token in input_program_tokens:
        if (re.findall(RE_Keywords, token)):
            Label(output, bg="white", text=token + " " + "-->" + " " + "Keyword", font=('Arial', 15)).pack()
        elif (re.findall(RE_Operators, token)):
            Label(output, bg="white", text=token + " " + "-->" + " " + "Operator", font=('Arial', 15)).pack()
        elif (re.findall(RE_Numerals, token)):
            Label(output, bg="white", text=token + " " + "-->" + " " + "Numeral", font=('Arial', 15)).pack()
        elif (re.findall(RE_Special_Characters, token)):
            Label(output, bg="white", text=token + " " + "-->" + " " + "Special Character/Symbol",
                  font=('Arial', 15)).pack()
        elif (re.findall(RE_Identifiers, token)):
            Label(output, bg="white", text=token + " " + "-->" + " " + "Identifiers", font=('Arial', 15)).pack()
            arrId1.append(token)
        else:
            Label(output, bg="white", text=print("Unknown Value", font=('Arial', 15))).pack()

        if (token == "="):
            arrVl.append(input_program_tokens[i])
            arrId2.append(input_program_tokens[i - 2])

        i = i + 1

    arrId3 = list(set(arrId1) - set(arrId2))

    for tok in arrId3:
        arrId4.append(tok)

def symbol():
    root2 = Tk()
    root2.title("Symbol Table")
    root2.geometry("610x450")
    root2.configure(background="blue")

    label = Label(root2, text="Symbol Table", font="timesnewroman 15 bold", background="blue", foreground="orchid", padx=20,pady=20)
    label.grid(row=0, column=1, pady=(30,0))


    tree_scroll = Scrollbar(root2, orient=VERTICAL)

    # tree2
    my_tree2 = ttk.Treeview(root2)

    my_tree2.configure(yscrollcommand=tree_scroll.set)

    style2 = ttk.Style()
    style2.theme_use("clam")

    tree_scroll.place(relx=0.823, rely=0.285, height=225, width=22)

    style2.configure("Treeview",
                    background="aqua",
                    foreground="black",
                    rowheight=38,
                    fieldbackgound="red",
                    )
    style2.map('Treeview',
              background=[('selected', 'green')])

    my_tree2['columns'] = ("name", "value")

    # format
    my_tree2.column("#0", width=0, minwidth=NO)
    my_tree2.column("name", anchor=CENTER, width=200)
    my_tree2.column("value", anchor=CENTER, width=200)

    # hedding
    my_tree2.heading("#0", text="", anchor=W)
    my_tree2.heading("name", text="Indentifiers Name", anchor=CENTER)
    my_tree2.heading("value", text="Value", anchor=CENTER)


    for token4 in arrId4:
        my_tree2.insert(parent='', index='end', text="", values=(token4, "Null"))

    j = 0

    for token2 in arrId2:
        my_tree2.insert(parent='', index='end', text="", values=(token2, arrVl[j]))
        j=j+1

    my_tree2.grid(row=1, column=1, padx=100, pady=30)

    tree_scroll.config(command=my_tree2.yview)

    root2.mainloop()


B = Button(top, text="Compile", command=lexicalAnalysis, width=15, font=('Arial', 15))
B.pack(pady=25, side=BOTTOM)
B2 = Button(top, text="Symbol table", command=symbol, width=15, font=('Arial', 15))
B2.pack(pady=25, side=BOTTOM)


def symbolTable():
    input_program_tokens = nltk.wordpunct_tokenize(entry1.get("1.0", "end-1c"))

    RE_Keywords = "auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include"
    RE_Operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"
    RE_Numerals = "^(\d+)$"
    RE_Special_Characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
    RE_Identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    RE_Headers = "([a-zA-Z]+\.[h])"
    RE_Datatype = "int|float|double|char|void"


B = Button(top, text="Generate", command=symbolTable, width=15, font=('Arial', 15))
B.pack(pady=25, side=BOTTOM)

top.mainloop()
