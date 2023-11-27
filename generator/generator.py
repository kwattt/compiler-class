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
    def __init__(self, lexic_tree, syntax_tree, symbol_table):
        self.lexic_tree = lexic_tree
        self.syntax_tree = syntax_tree
        self.symbol_table = symbol_table
        self.pseudocode = []
        self.pseudocode.append("CODE")
        self.generate_pseudocode()
        self.write_pseudocode()

    def generate_pseudocode(self):
        self.generate_pseudocode_from_tree(self.syntax_tree)

    def generate_pseudocode_from_tree(self, node):
        if node.type == "program":
            self.generate_pseudocode_from_tree(node.children[0])
        elif node.type == "declaration":
            self.generate_pseudocode_from_tree(node.children[0])
        elif node.type == "var":
            self.pseudocode.append("PUSHC 0")
            self.pseudocode.append("STORE " + node.value)
        elif node.type == "assignment":
            self.generate_pseudocode_from_tree(node.children[0])
            self.generate_pseudocode_from_tree(node.children[1])
        elif node.type == "cin":
            self.pseudocode.append("INPUT")
            self.pseudocode.append("STORE " + node.value)
        elif node.type == "cout":
            self.generate_pseudocode_from_tree(node.children[0])
            self.pseudocode.append("OUTPUT")
        elif node.type == "expression":
            self.generate_pseudocode_from_tree(node.children[0])
        elif node.type == "term":
            self.generate_pseudocode_from_tree(node.children[0])
        elif node.type == "factor":
            self.generate_pseudocode_from_tree(node.children[0])
        elif node.type == "number":
            self.pseudocode.append("PUSHC " + node.value)
        elif node.type == "identifier":
            self.pseudocode.append("LOAD " + node.value)
        elif node.type == "addition":
            self.generate_pseudocode_from_tree(node.children[0])
            self.generate_pseudocode_from_tree(node.children[1])
            self.pseudocode.append("ADD")
        elif node.type == "subtraction":
            self.generate_pseudocode_from_tree(node.children[0])
            self.generate_pseudocode_from_tree(node.children[1])
            self.pseudocode.append("SUB")
        elif node.type == "multiplication":
            self.generate_pseudocode_from_tree(node.children[0])
            self.generate_pseudocode_from_tree(node.children[1])
            self.pseudocode.append("MUL")
        elif node.type == "division":
            self.generate_pseudocode_from_tree(node.children[0])
            self.generate_pseudocode_from_tree(node.children[1])
            self.pseudocode.append("DIV")
        elif node.type == "modulo":
            self.generate_pseudocode_from_tree(node.children[0])
            self.generate_pseudocode_from_tree(node.children[1])
            self.pseudocode.append("MOD")
        elif node.type == "negative":
            self.generate_pseudocode_from_tree(node.children[0])
            self.pseudocode.append("NEG")

    def write_pseudocode(self):
        f = open("pseudocode.txt", "w")
        for line in self.pseudocode:
            f.write(line + "\n")
        f.close()

    def print_pseudocode(self):
        for line in self.pseudocode:
            print(line)