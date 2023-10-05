class Node:
    pass

class ProgramNode(Node):
    def __init__(self):
        self.children = []

    def __repr__(self):
        return f"Program({self.children})"

class StatementNode(Node):
    pass

class AssignmentNode(StatementNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"Assignment({self.identifier}, {self.expression})"

class IfStatementNode(StatementNode):
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.true_branch}, {self.false_branch})"

class CommentNode(StatementNode):
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f"Comment({self.content})"

class IdentifierNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Identifier({self.value})"

class ExpressionNode(Node):
    pass

class LogicExpressionNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"LogicExpression({self.left}, {self.operator}, {self.right})"

class RelationalExpressionNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"RelationalExpression({self.left}, {self.operator}, {self.right})"

class ArithmeticExpressionNode(ExpressionNode):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"ArithmeticExpression({self.left}, {self.operator}, {self.right})"

class TermNode(ExpressionNode):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Term({self.left}, {self.operator}, {self.right})"

class FactorNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Factor({self.value})"

class NumberNode(FactorNode):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return f"Number({self.value})"

class FloatNode(FactorNode):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return f"Float({self.value})"

class StringNode(FactorNode):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return f"String({self.value})"

class BooleanNode(FactorNode):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return f"Boolean({self.value})"