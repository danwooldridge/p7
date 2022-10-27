from concurrent.futures import process
from logging import raiseExceptions
from webbrowser import get
from ParseTree import *





class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.myList = tokens
        self.currentToken = ""
        self.type = ["int", "char", "boolean", "identifier"]
        self.statements = ["let", "if", "while", "do", "return"]
        self.op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
        self.unaryOp = ["-", "~"]
        self.keywordConstant = ["true", "false", "null", "this"]
        self.subroutineCall = []

        pass

    def process(self, str):
        #print(str)
        self.currentToken = self.myList[0].getValue()
        if self.currentToken in str:
            newTree = ParseTree(tokens[0].getType(), tokens[0].getValue())
            self.myList.pop(0)
            return newTree
        else:
            raise Exception
    def process2(self, str):
        #print(str)
        self.currentToken = self.myList[0].getType()

        if self.currentToken in str:
            newTree = ParseTree(tokens[0].getType(), tokens[0].getValue())
            self.myList.pop(0)
            return newTree
        else:
            raise Exception

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        self.currentToken = self.myList[0]
        if self.myList[0].getValue() != "class":
                raise Exception
        return self.compileClass()
        
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        tree = ParseTree("class", None)
        
        tree.addChild(self.process("class"))
        tree.addChild(self.process("Main"))
        tree.addChild(self.process("{"))
        while(tokens[0].getValue() in ('static', 'field')):
            tree.addChild(self.compileClassVarDec())
        while(tokens[0].getValue() in ('constructor', 'function', 'method')):
            tree.addChild(self.compileSubroutine())
        tree.addChild(self.process("}"))
    
        return tree 
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        tokens = self.myList
        tree = ParseTree("classVarDec", None)

        tree.addChild(self.process(["static", "field"]))
        tree.addChild(self.process(self.type))
        tree.addChild(self.process2("identifier"))
        tree.addChild(self.process(";"))

        return tree
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        tokens = self.myList
        tree = ParseTree("subroutine", None)

        tree.addChild(self.process(["constructor", "function", "method"]))
        tree.addChild(self.process("void" + str(self.type)))
        tree.addChild(self.process2("identifier"))
        tree.addChild(self.process("("))

        tree.addChild(self.compileParameterList())
        while tokens[0].getValue() == ',':
            tree.addChild(self.process(","))
            tree.addChild(self.compileParameterList())

        tree.addChild(self.process(")"))
        tree.addChild(self.compileSubroutineBody())

        return tree
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        tokens = self.myList
        tree = ParseTree("parameterList", None)
        tree.addChild(self.process(self.type))
        tree.addChild(self.process2("identifier"))
        return tree 
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        tokens = self.myList
        tree = ParseTree("subroutineBody", None)

        tree.addChild(self.process("{"))

        tree.addChild(self.compileVarDec())

        while tokens[0].getValue() == ',':
            tree.addChild(self.process(","))
            tree.addChild(self.compileVarDec())
        tree.addChild(self.compileStatements())
        tree.addChild(self.process("}"))

        return tree
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        tokens = self.myList
        tree = ParseTree("varDec", None)
        tree.addChild(self.process("var"))
        tree.addChild(self.process(self.type))
        tree.addChild(self.process2("identifier"))
        tree.addChild(self.process(";"))

        return tree
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        tokens = self.myList
        tree = ParseTree("statements", None)

        while tokens[0].getValue() == "let":
            tree.addChild(self.compileLet())

        while tokens[0].getValue() == "if":
            tree.addChild(self.compileIf())
        
        while tokens[0].getValue() == "while":
            tree.addChild(self.compileWhile())
        
        while tokens[0].getValue() == "do":
            tree.addChild(self.compileDo())
        
        while tokens[0].getValue() == "return":
            tree.addChild(self.compileReturn())

        return tree 
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        tokens = self.myList
        tree = ParseTree("letStatement", None)
        tree.addChild(self.process("let"))
        tree.addChild(self.process2("identifier"))
        tree.addChild(self.process("="))
        tree.addChild(self.compileExpression())
        tree.addChild(self.process(";"))


        return tree
    

    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        tokens = self.myList
        tree = ParseTree("ifStatement", None)
        tree.addChild(self.process("if"))
        tree.addChild(self.process("("))
        tree.addChild(self.compileExpression())

        tree.addChild(self.process(")"))
        tree.addChild(self.process("{"))

        tree.addChild(self.compileStatements())
        tree.addChild(self.process("}"))
        if tokens[0].getValue() == "else":
            tree.addChild(self.process("else"))
            tree.addChild(self.process("{"))
            tree.addChild(self.compileStatements())
            while tokens[0].getValue() in self.statements:
                tree.addChild(self.compileStatements())

        tree.addChild(self.process("}"))


        return tree
    
    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """

        tokens = self.myList
        tree = ParseTree("whileStatement", None)
        tree.addChild(self.process("while"))
        tree.addChild(self.process("("))
        tree.addChild(self.compileExpression())
        tree.addChild(self.process(")"))
        tree.addChild(self.process("{"))
        tree.addChild(self.compileStatements())
        tree.addChild(self.process("}"))

        return tree
    

    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        tokens = self.myList
        tree = ParseTree("doStatement", None)
        tree.addChild(self.process("do"))
        tree.addChild(self.compileExpression())
        tree.addChild(self.process(";"))


        return tree 
    

    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        tokens = self.myList
        tree = ParseTree("skipStatement", None)
        tree.addChild(self.process("return"))
        if tokens[0].getValue() == "skip":
            tree.addChild(self.compileExpression())
        tree.addChild(self.process(";"))

        return tree
    

    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        tokens = self.myList
        tree = ParseTree("expression", None)
        tree.addChild(self.process("skip"))

        return tree 
    

    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None 
    

    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None 
    

if __name__ == "__main__":
  

    """ 
 class Main {
    static int a ;
}
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","Main"))
    tokens.append(Token("symbol","{"))

    tokens.append(Token("keyword","static"))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",";"))

    tokens.append(Token("keyword","function"))
    tokens.append(Token("keyword","void"))
    tokens.append(Token("identifier","myFunc"))
    tokens.append(Token("symbol","("))

    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",")"))
    tokens.append(Token("symbol","{"))

    tokens.append(Token("keyword","var"))
    tokens.append(Token("keyword","int"))
    tokens.append(Token("identifier","a"))
    tokens.append(Token("symbol",";"))
    

    ## if statement ##
    # tokens.append(Token("keyword","if"))
    # tokens.append(Token("symbol","("))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol",")"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("keyword","let"))
    # tokens.append(Token("identifier","a"))
    # tokens.append(Token("symbol","="))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol",";"))
    # tokens.append(Token("symbol","}"))
    # tokens.append(Token("keyword","else"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("keyword","let"))
    # tokens.append(Token("identifier","a"))
    # tokens.append(Token("symbol","="))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol",";"))
    # tokens.append(Token("symbol","}"))


    ## while statement ##
    # tokens.append(Token("keyword","while"))
    # tokens.append(Token("symbol","("))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol",")"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("keyword","let"))
    # tokens.append(Token("identifier","a"))
    # tokens.append(Token("symbol","="))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol",";"))
    # tokens.append(Token("symbol","}"))

    ## do statment ##
    # tokens.append(Token("keyword","do"))
    # tokens.append(Token("keyword","skip"))
    # tokens.append(Token("symbol",";"))

    ## return statement ##
    tokens.append(Token("keyword","return"))
    tokens.append(Token("keyword","skip"))
    tokens.append(Token("symbol",";"))


    tokens.append(Token("symbol","}"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    #parser = process(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
