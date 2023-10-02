# Define syntax tree nodes

class Node:
    pass

class ProgramNode(Node):
    def __init__(self):
        self.children = []

    def __repr__(self):
        return f"Program({self.children})"

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"Assignment({self.identifier}, {self.expression})"

class IdentifierNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Identifier({self.value})"

class ExpressionNode(Node):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        if self.operator:
            return f"Expression({self.left}, {self.operator}, {self.right})"
        return f"Expression({self.left})"

class TermNode(Node):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        if self.operator:
            return f"Term({self.left}, {self.operator}, {self.right})"
        return f"Term({self.left})"

class FactorNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Factor({self.value})"

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"
