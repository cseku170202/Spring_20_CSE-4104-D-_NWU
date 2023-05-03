from tkinter import*
from tkinter import ttk
import re
import nltk

root = Tk()
root.title("Compiler Design")
root.geometry("1370x680")
root.configure(background="purple")

label1 = Label(root, text="Code", font="timesnewroman 15 bold",background="purple",foreground="orchid", padx=20, pady=20)
label1.grid(row=0, column=1,padx=(80,0))
label2 = Label(root, text="Lexical Analysis", font="timesnewroman 15 bold",background="purple",foreground="orchid", padx=20, pady=20)
label2.grid(row=0, column=4,padx=(200,0), pady=(30))

entry = Text(root,  width=48, borderwidth=5)
entry.grid(row=1, column=1,pady=3, padx=(80,0))

tree_scroll = Scrollbar(root, orient=VERTICAL)

#tree 1
my_tree = ttk.Treeview(root)

my_tree.configure(yscrollcommand=tree_scroll.set)

tree_scroll.configure(command=my_tree.yview)

style1 = ttk.Style()
style1.theme_use("clam")

tree_scroll.place(relx=0.934, rely=0.188, height=408, width=22)

style1.configure("Treeview",
                background="aqua",
                foreground="black",
                rowheight=38,
                fieldbackgound="red"
                )
style1.map('Treeview',
          background=[('selected', 'green')])

my_tree['columns'] = ("Tokens","Analyze", "line")

# format
my_tree.column("#0", width=0, minwidth=NO)
my_tree.column("Tokens", anchor=CENTER, width=200)
my_tree.column("Analyze", anchor=CENTER, width=200)
my_tree.column("line", anchor=CENTER, width=200)

# hedding
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Tokens", text="Tokens", anchor=CENTER)
my_tree.heading("Analyze", text="Analyze name", anchor=CENTER)
my_tree.heading("line", text="Line", anchor=CENTER)


arrId1 = []
arrId2 = []
arrId3 = []
arrId4 = []
arrVl = []


def show():

    input_program = entry.get(1.0, END)

    input_program_tokens = nltk.wordpunct_tokenize(input_program);

    RE_Keywords = "auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include"
    RE_Operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)|(<)|(>)"
    RE_Numerals = "^(\d+)$"
    RE_Special_Characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
    RE_Identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    RE_mfunction = "main"
    RE_bfun = "scanf|printf"

    count = 0
    i = 1

    for token in input_program_tokens:


        if (re.findall(RE_mfunction, token)):
            my_tree.insert(parent='', index='end', text="", values=(token, "main function", count))

        elif(input_program_tokens[i-1]=="A" and input_program_tokens[i-2] == '"'):
            my_tree.insert(parent='', index='end', text="", values=(token, "String", count))
        elif(input_program_tokens[i-1]==">" and input_program_tokens[i-2] == "A"):
            my_tree.insert(parent='', index='end', text="", values=(token, "String", count))
        elif (input_program_tokens[i - 1] == "B" and input_program_tokens[i - 2] == ">"):
            my_tree.insert(parent='', index='end', text="", values=(token, "String", count))
        elif (input_program_tokens[i - 1] == "B" and input_program_tokens[i - 2] == '"'):
            my_tree.insert(parent='', index='end', text="", values=(token, "String", count))
        elif (input_program_tokens[i - 1] == ">" and input_program_tokens[i - 2] == "A"):
            my_tree.insert(parent='', index='end', text="", values=(token, "String", count))
        elif (input_program_tokens[i - 1] == "A" and input_program_tokens[i - 2] == ">"):
            my_tree.insert(parent='', index='end', text="", values=(token, "String", count))

        elif (re.findall(RE_bfun, token)):
            my_tree.insert(parent='', index='end', text="", values=(token, "Built in Function", count))

        elif (re.findall(RE_Keywords, token)):
            my_tree.insert(parent='', index='end', text="", values=(token,"Keyword", count))

        elif (re.findall(RE_Operators, token)):
            my_tree.insert(parent='', index='end', text="", values=(token, "Operator", count))

        elif (re.findall(RE_Numerals, token)):
            my_tree.insert(parent='', index='end', text="", values=(token, "Numeral", count))
            #arrVl.append(token)

        elif (re.findall(RE_Special_Characters, token)):
            my_tree.insert(parent='', index='end', text="", values=(token, "Special Character/Symbol", count))

        elif (re.findall(RE_Identifiers, token)):
            my_tree.insert(parent='', index='end', text="", values=(token, "Identifiers", count))
            arrId1.append(token)

        else:
            my_tree.insert(parent='', index='end', text="", values=(token, "Invalid", count))

        if (token == ";"):
            count = count + 1
        if (input_program_tokens[i-1] == "{" and input_program_tokens[i-2] == ")" and input_program_tokens[i-3] == "(" and input_program_tokens[i-4] == "main") :
            count = count + 1


        if (token == "="):
            arrVl.append(input_program_tokens[i])
            arrId2.append(input_program_tokens[i-2])

        i = i + 1


    arrId3 = list(set(arrId1) - set (arrId2))

    for tok in arrId3:
        arrId4.append(tok)


def clear():

    for record in my_tree.get_children():
        my_tree.delete(record)


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

my_tree.grid(row=1, column=4, padx=(200,0))

btn1 = Button(root, text="Analyze", font="times 15 bold", bg="orchid", command=show)
btn1.grid(row=2, column=1, ipadx=30, pady=40, padx=(50,0))
btn2 = Button(root, text="Clear", font="times 15 bold", bg="orchid", command=clear)
btn2.grid(row=2, columnspan=3, column=2, ipadx=40, pady=40, padx=(20,0))
btn3 = Button(root, text="Symbol Table", font="times 15 bold", bg="orchid", command=symbol)
btn3.grid(row=2, columnspan=3, column=2, ipadx=40, pady=40, padx=(550,0))

root.mainloop()
