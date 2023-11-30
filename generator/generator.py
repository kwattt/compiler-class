# Path: generator/generator.py
from semantic import *
from syntax import *
from lexic import *

## takes the lexic tree, the syntax tree, and the symbol table and generates the pseudocode with keywords CODE, PUSHC, PUSHA, LOAD, STORE, NEG, ADD, MUL, DIV, MOD, INPUT, OUTPUT, END. 

## for example

# int a; 
# cin = a;
# int b;
# cin = b;
# int c;
# c = a + b;
# print(c)

# will be translated to

# CODE
# PUSHC 0
# STORE a
# PUSHC 0
# STORE b
# LOAD a
# LOAD b
# ADD
# STORE c
# LOAD c
# OUTPUT
# END
# the pseudocode will be written to a file called pseudocode.txt

class Generator:
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
        self.pseudocode = []
        self.pseudocode.append(".CODE")
        #self.write_pseudocode()
        self.generate_pseudocode()
        self.pseudocode.append("END")
        self.print_pseudocode()
        self.pseudoasm = []

    def generate_pseudoasm(self):
        ## for example PUSHC 0, STORE A should be MOV A, 0
        # remeber every line is a different item in the list, if it starts wuth PUSHC, A should be in the next item and so on
        cindex = 0
        while cindex < len(self.pseudocode):
            line = self.pseudocode[cindex]
            line_split = line.split(' ')
            ## check if there is an add
            print(cindex, line)
            if line_split[0] == "ADD":
                ## -1 is load, ignore, -2 is right term, -3 is left term, -4 is target variable
                self.pseudoasm.append(f"MOV {self.pseudocode[cindex-4].split(' ')[1]}, {self.pseudocode[cindex-2].split(' ')[1]}")
                self.pseudoasm.append(f"ADD {self.pseudocode[cindex-5].split(' ')[1]}, {self.pseudocode[cindex-4].split(' ')[1]}")
                cindex += 6
            elif line_split[0] == "SUB":
                self.pseudoasm.append(f"MOV {self.pseudocode[cindex-4].split(' ')[1]}, {self.pseudocode[cindex-2].split(' ')[1]}")
                self.pseudoasm.append(f"SUB {self.pseudocode[cindex-5].split(' ')[1]}, {self.pseudocode[cindex-4].split(' ')[1]}")
                cindex += 6
            elif line_split[0] == "MUL":
                self.pseudoasm.append(f"MOV {self.pseudocode[cindex-4].split(' ')[1]}, {self.pseudocode[cindex-2].split(' ')[1]}")
                self.pseudoasm.append(f"MUL {self.pseudocode[cindex-5].split(' ')[1]}, {self.pseudocode[cindex-4].split(' ')[1]}")
                cindex += 6
            elif line_split[0] == "DIV":
                self.pseudoasm.append(f"MOV {self.pseudocode[cindex-4].split(' ')[1]}, {self.pseudocode[cindex-2].split(' ')[1]}")
                self.pseudoasm.append(f"DIV {self.pseudocode[cindex-5].split(' ')[1]}, {self.pseudocode[cindex-4].split(' ')[1]}")
                cindex += 6

            elif line_split[0] == "PUSHC":
                self.pseudoasm.append(f"MOV {self.pseudocode[cindex+1].split(' ')[1]}, {self.pseudocode[cindex].split(' ')[1]}")
                cindex+= 3
            else: 
                cindex += 1

        return self.pseudoasm

    def get_pseudo(self):
        return self.pseudocode

    def generate_pseudocode(self):
        self.generate_pseudocode_from_tree(self.syntax_tree)

    def parse_term(self, node):
        ## it is for * and / 
        if isinstance(node, TermNode):
            self.parse_term(node.left)
            self.parse_term(node.right)
            self.parse_operation(node.operator)

    def parse_operation(self, operator):
        if operator == "+":
            self.pseudocode.append(f"ADD")
        elif operator == "-":
            self.pseudocode.append(f"SUB")
        elif operator == "*":
            self.pseudocode.append(f"MUL")
        elif operator == "/":
            self.pseudocode.append(f"DIV")
        elif operator == "%":
            self.pseudocode.append(f"MOD")

    def parse_expression(self, node):
        if isinstance(node, ArithmeticExpressionNode):
            self.parse_expression(node.left)
            self.parse_expression(node.right)
            self.parse_operation(node.operator)
        elif isinstance(node, FactorNode):
            if isinstance(node, IntNode):
                self.pseudocode.append(f"PUSHC {node.value}")
            elif isinstance(node, FloatNode):
                self.pseudocode.append(f"PUSHC {node.value}")
            elif isinstance(node.value, IdentifierNode):
                self.pseudocode.append(f"PUSHA {node.value.value}")
                self.pseudocode.append(f"LOAD")
            else:
                self.pseudocode.append(f"?")
        elif isinstance(node, TermNode):
            self.parse_expression(node.left)
            self.parse_expression(node.right)

            self.parse_term(node)

    def generate_pseudocode_from_tree(self, node):
        ## check if node is a program
        if isinstance(node, ProgramNode):
            for child in node.children:
                self.generate_pseudocode_from_tree(child)
        ## check if node is a statement
        elif isinstance(node, InitializationNode):
            self.generate_pseudocode_from_tree(node.identifier)
            if node.expression:
                self.pseudocode.append(f"PUSHC {node.expression.value.value}")
            else:
                self.pseudocode.append(f"PUSHC 0")
            self.pseudocode.append(f"STORE {node.identifier.value}")

        elif isinstance(node, AssignmentNode):
            self.pseudocode.append(f"PUSHA {node.identifier.value}")
            self.parse_expression(node.expression)
            self.pseudocode.append(f"STORE")
            self.pseudocode.append(f"OUTPUT {node.identifier.value}")

        elif isinstance(node, ArithmeticExpressionNode):
            self.parse_expression(node)

        elif isinstance(node, CinNode):
            self.generate_pseudocode_from_tree(node.identifier)
            self.pseudocode.append(f"INPUT")
            self.pseudocode.append(f"STORE {node.identifier.value}")

    def write_pseudocode(self):
        f = open("pseudocode.txt", "w")
        for line in self.pseudocode:
            f.write(line + "\n")
        f.close()

    def print_pseudocode(self):
        for line in self.pseudocode:
            print(line)