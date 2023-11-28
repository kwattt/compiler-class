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

    def generate_pseudocode(self):
        self.generate_pseudocode_from_tree(self.syntax_tree)

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

    def generate_pseudocode_from_tree(self, node):
        ## check if node is a program
        if isinstance(node, ProgramNode):
            for child in node.children:
                self.generate_pseudocode_from_tree(child)
        ## check if node is a statement
        elif isinstance(node, InitializationNode):
            self.generate_pseudocode_from_tree(node.identifier)
            if node.expression:
                self.pseudocode.append(f"PUSHC {node.expression.value}")
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