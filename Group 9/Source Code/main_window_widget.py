from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow,QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QTableWidget, QTableWidgetItem, QLabel
from PySide6.QtCore import Slot
import re
from subprocess import PIPE, run

class MainWindowWidget(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Lexical Analyzer")
        self.setMinimumHeight(400)
        self.setMinimumWidth(750)
        content = MainWindowContentWidget()
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("Options")
        quitAction = fileMenu.addAction("Quit")
        quitAction.triggered.connect(self.quitClicked)
        self.setCentralWidget(content)

    @Slot()
    def quitClicked(self):
        self.app.quit()


class MainWindowContentWidget(QWidget):
    cDataTypeKeywords = ["char","double","float","int","long","short"]
    specialSymbolDictionary = {
        "#": "Special character: hash",
        "<": "Special character: smaller than",
        ">": "Special character: greater than",
        ".": "Special character: period/dot",
        ";": "Special character: semicolon",
        "(": "Special character: parentheses start",
        ")": "Special character: parentheses end",
        "{": "Special character: curly bracket start",
        "}": "Special character: curly bracket end",
        "[": "Special character: square bracket start",
        "]": "Special character: square bracket end",
        ",": "Special character: comma",
        "=": "Oparetor: equal",
        "+": "Oparetor: plus",
        "-": "Oparetor: minus",
        "*": "Oparetor: product",
        "/": "Special character: slash/divide",
        "*": "Special character: asterisk",
        "\"": "Special character: Double quote",
        "\'": "Special character: Single quote",
        "%": "Special character: percentage",
        "&": "Oparetor: and",
        "!=": "Oparetor: Not equal",
    }
    specialCasesDicionary = {
        "main": "Function",
        "printf": "Library function",
        "scanf": "Library function",
    }

    def __init__(self):
        super().__init__()
        analyzeButton = QPushButton("Analyze")
        self.sourceCodeEditor = QPlainTextEdit()
        self.sourceCodeEditor.setStyleSheet("background-color: darkblue;color: #FFFFFF;")
        analyzeButton.clicked.connect(self.button1Clicked)
        codeLabel = QLabel("Code")
        codeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        leftVerticleLayout = QVBoxLayout()
        leftVerticleLayout.addWidget(codeLabel)
        leftVerticleLayout.addWidget(self.sourceCodeEditor)
        leftVerticleLayout.addWidget(analyzeButton)

        self.analyzedTable = QTableWidget()
        self.analyzedTable.setColumnCount(3)
        self.analyzedTable.setHorizontalHeaderLabels(["Identifier","Analyze name","Line"])
        self.analyzedTable.setStyleSheet("background-color: lightblue;")

        rightVerticleLayout = QVBoxLayout()

        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.resetButtonClicked)
        symbolTableButton = QPushButton("Identifier table")
        symbolTableButton.clicked.connect(self.symbolTableButtonClicked)
        symbolTableLabel = QLabel("Symbol table")
        symbolTableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rightVerticleLayout.addWidget(symbolTableLabel)
        rightVerticleLayout.addWidget(self.analyzedTable)
        rightVerticleLayout.addWidget(resetButton)
        rightVerticleLayout.addWidget(symbolTableButton)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addLayout(leftVerticleLayout)
        horizontalLayout.addLayout(rightVerticleLayout)
        self.setLayout(horizontalLayout)

    @Slot()
    def button1Clicked(self):
        self.analyzeSourceCode(self.sourceCodeEditor.toPlainText())


    @Slot()
    def symbolTableButtonClicked(self):
        self.symbolTableWindow = SymbolTableWindowWidget(self.sourceCodeEditor.toPlainText())
        self.symbolTableWindow.show()


    @Slot()
    def resetButtonClicked(self):
        self.sourceCodeEditor.clear()
        self.setAnalyzedDataToTable([])

    def setAnalyzedDataToTable(self, analyzedData):
        self.analyzedTable.clear()
        self.analyzedTable.setRowCount(len(analyzedData))
        for i, (identifierData, dataTypeData, valueData) in enumerate(analyzedData):
            identifier= QTableWidgetItem(identifierData)
            dataType= QTableWidgetItem(dataTypeData)
            value = QTableWidgetItem(valueData)
            self.analyzedTable.setItem(i, 0, identifier)
            self.analyzedTable.setItem(i, 1, dataType)
            self.analyzedTable.setItem(i, 2, value)
        self.analyzedTable.setHorizontalHeaderLabels(["Identifier","Analyze name","Line"])
    
    def isEmpty(token):
        return token==""

    def analyzeSourceCode(self, sourceCode: str):
        analyzedData = []
        delimeter = "([^a-zA-Z-0-9])"
        sourceCodeTextList = sourceCode.split("\n")
        for line, sourceCodeLine in enumerate(sourceCodeTextList,start=1):
            sourceCodeLineText = sourceCodeLine.strip()
            isSpecialCase = self.isLineSpecialCase(sourceCodeLineText)
            if isSpecialCase:
                (identifier, token) = self.getLineSpeicalCaseAnalyzedData(sourceCodeLineText)
                analyzedData.append((identifier,token,str(line)))
            else:
                try:
                    lineTextTokenList = re.split(delimeter,sourceCodeLineText)
                    lineTextTokenList = list(filter(lambda token: token!="" and token!=" ",lineTextTokenList))
                    print(lineTextTokenList)
                    for token in lineTextTokenList:
                        isTokenSpecial = self.isTokenSpecialCase(token)
                        if(isTokenSpecial):
                            label = self.getTokenSpecialCaseAnalyzedData(token)
                            analyzedData.append((token, label, str(line)))
                        else:
                            if(self.isCKeyword(token)):
                                analyzedData.append((token,"Keyword",str(line)))
                            if(self.isSpecialSymbol(token)):
                                analyzedData.append((token,self.getSpecialSymbolName(token),str(line)))
                            if(self.isTokenVariable(token)):
                                analyzedData.append((token,"Identifier",str(line)))
                            if (self.isTokenOtherCase(token)):
                                analyzedData.append((token, self.getTokenTypeFromOtherCase(token), str(line)))
                except Exception:
                    pass
        print(sourceCode)
        self.setAnalyzedDataToTable(analyzedData)

    def isLineSpecialCase(self, line):
        if line.startswith("#"):
            return True
        # elif line.startswith("printf"):
        #     return True
        # elif line.startswith("scanf"):
        #     return True
        # elif line.find("main") != -1:
        #     return True
        return False

    def getLineSpeicalCaseAnalyzedData(self, line):
        identifier = ""
        label = ""
        if (line.startswith("#")):
            identifier = line
            label = "Header line"
        # elif (line.startswith("printf")):
        #     identifier = line
        #     label = "library function"
        # elif (line.startswith("scanf")):
        #     identifier = line
        #     label = "library function"
        # elif line.find("main") != -1:
        #     identifier = line
        #     label = "main function"
        return (identifier,label)

    def isTokenOtherCase(self, token:str):
        if token.isdigit():
            return True
        return False


    def getTokenTypeFromOtherCase(self, token: str) -> str:
        if token.isdigit():
            return "Numerical"
        return ""

    def isTokenSpecialCase(self, token):
        return token in self.specialCasesDicionary

    def getTokenSpecialCaseAnalyzedData(self, token):
        EmptyLabel = ""
        specialCase = self.specialCasesDicionary.get(token)
        if(specialCase==None):
            return EmptyLabel
        return specialCase

    def isTokenCKeyword(self, token: str):
        try:
            self.cDataTypeKeywords.index(token)
            return True
        except ValueError:
            return False

    def isCKeyword(self, token):
        cKeywords = ["auto","break","case","char","const","continue","default","do","double","else", "enum","extern","float","for","goto", "if","int","long","register","return", "short","signed","sizeof","static","struct", "switch","typedef","union","unsigned","void", "volatile","while", "include", "main"]
        return (token in cKeywords)

    def isTokenVariable(self, token: str):
        if(self.isCKeyword(token)):
            return False
        if(self.isSpecialSymbol(token)):
            return False
        if(token==""):
            return False
        firstCharacter = token[0]
        return firstCharacter == "_" or firstCharacter.isalpha()

    def getSpecialSymbolName(self, token):
        symbolName = self.specialSymbolDictionary.get(token)
        if(symbolName == None):
            return ""
        return symbolName
    
    def isSpecialSymbol(self,token):
        return token in self.specialSymbolDictionary

    def isTokenValue(self, token: str):
        # if(self.isTokenVariable(token)):
            # return False
        if(self.isFloat(token)):
            return True
        if(self.isInteger(token)):
            return True
        if(self.isFloat(token)):
            return True
        if("\"" in token):
            return True
        if("\'" in token):
            return True
        return False
    
    def isFloat(self, string: str):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def isInteger(self, string: str):
        try:
            int(string)
            return True
        except ValueError:
            return False


class SymbolTableWindowWidget(QWidget):
    cDataTypeKeywords = ["char","double","float","int","long","short"]
    def __init__(self,sourceCodeText):
        super().__init__()
        self.sourceCodeText = sourceCodeText

        verticleLayout = QVBoxLayout()
        self.analyzedTable = QTableWidget()
        self.analyzedTable.setColumnCount(3)
        self.analyzedTable.setHorizontalHeaderLabels(["Identifier","Data Type","Value"])
        self.analyzedTable.setStyleSheet("background-color: lightskyblue;")
        verticleLayout.addWidget(self.analyzedTable)
        self.setWindowTitle("Identifier table")
        self.setMinimumHeight(300)
        self.setMinimumWidth(450)
        self.setLayout(verticleLayout)
        self.analyzeSourceCode(self.sourceCodeText)

    def setAnalyzedDataToTable(self, analyzedData):
        self.analyzedTable.clear()
        self.analyzedTable.setRowCount(len(analyzedData))
        for i, (identifierData, dataTypeData, valueData) in enumerate(analyzedData):
            identifier= QTableWidgetItem(identifierData)
            dataType= QTableWidgetItem(dataTypeData)
            value = QTableWidgetItem(valueData)
            self.analyzedTable.setItem(i, 0, identifier)
            self.analyzedTable.setItem(i, 1, dataType)
            self.analyzedTable.setItem(i, 2, value)
        self.analyzedTable.setHorizontalHeaderLabels(["Identifier","Data Type","Value"])
    
    def analyzeSourceCode(self, sourceCode: str):
        analyzedData = []
        delimeter = r" |,|;|=|\+|-|\*|/|%|\(|\)"
        sourceCodeTextList = sourceCode.split("\n")
        for sourceCodeLine in sourceCodeTextList:
            sourceCodeLineText = sourceCodeLine.strip()
            isSpecialCase = self.isSpecialCase(sourceCodeLineText)
            if not isSpecialCase:
                try:
                    lineTextTokenList = re.split(delimeter,sourceCodeLineText)
                    isCDataTypeKeywordFound = False
                    identifier = ""
                    dataType = ""
                    value = ""
                    for lineTextToken in lineTextTokenList:
                        if(self.isTokenCKeyword(lineTextToken)):
                            dataType = lineTextToken
                            isCDataTypeKeywordFound = True
                        elif(isCDataTypeKeywordFound):
                            if(self.isTokenVariable(lineTextToken)):
                                if(identifier==""):
                                    identifier = lineTextToken
                                else:
                                    identifier = identifier + " " + lineTextToken
                            elif(self.isTokenValue(lineTextToken)):
                                if(value==""):
                                    value = lineTextToken
                                else:
                                    value = value + " " + lineTextToken
                    if(not(identifier == "" and dataType == "" and value == "")):
                        analyzedData.append((identifier,dataType,value))
                except Exception:
                    pass
        print(sourceCode)
        self.setAnalyzedDataToTable(analyzedData)

    def isSpecialCase(self, line):
        if line.startswith("#"):
            return True
        elif line.startswith("printf"):
            return True
        elif line.startswith("scanf"):
            return True
        elif line.find("main") != -1:
            return True
        return False
    def isTokenCKeyword(self, token: str):
        try:
            self.cDataTypeKeywords.index(token)
            return True
        except ValueError:
            return False

    def isTokenVariable(self, token: str):
        if(token==""):
            return False
        firstCharacter = token[0]
        return firstCharacter == "_" or firstCharacter.isalpha()

    def isTokenValue(self, token: str):
        if(self.isFloat(token)):
            return True
        if(self.isInteger(token)):
            return True
        if(self.isFloat(token)):
            return True
        if("\"" in token):
            return True
        if("\'" in token):
            return True
        return False
    
    def isFloat(self, string: str):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def isInteger(self, string: str):
        try:
            int(string)
            return True
        except ValueError:
            return False

