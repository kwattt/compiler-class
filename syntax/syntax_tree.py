## Node class with attributes to get all the children of a node, and a __repr__ method to print the node in a readable format
from typing import List

class Node(object):
    def children(self):
        pass

    def __repr__(self):
        return self.__str__()

def program_to_tree(node: Node, indent=0):
    attributes = vars(node)
    tree = {
        type(node).__name__: None
    }
    subtree = {}
    for at in attributes:
        # if its a list, iterate
        if isinstance(attributes[at], list):
            for child in attributes[at]:
                #subtree.append(program_to_tree(child, indent + 1))
                if Node in type(child).__mro__:
                    if at not in subtree:
                        subtree[at] = [program_to_tree(child, indent + 1)]
                    else:
                        subtree[at].append(program_to_tree(child, indent + 1))
        else:
            # check if it is a node
            if Node in type(attributes[at]).__mro__:
                #tree.append(program_to_tree(attributes[at], indent + 1))
                subtree[at] = program_to_tree(attributes[at], indent + 1)
            else:
                #subtree.append({at: attributes[at]})
                subtree[at] = attributes[at]
    if len(subtree) > 0:
        tree[type(node).__name__] = subtree
    return tree

class ProgramNode(Node):
    def __init__(self):
        self.children : List[Node] = []

    def __repr__(self):
        return f"Program({self.children})"

class StatementNode(Node):
    pass

###### assignment    -> identifier = expression;
class AssignmentNode(StatementNode):
    def __init__(self, identifier, expression):
        self.identifier : IdentifierNode = identifier
        self.expression : ExpressionNode = expression

    def __repr__(self):
        return f"Assignment({self.identifier}, {self.expression})"

class IfStatementNode(StatementNode):
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition: ExpressionNode = condition
        self.true_branch : StatementNode = true_branch
        self.false_branch : StatementNode = false_branch

    def __repr__(self):
        return f"IfStatementNode({self.condition}, {self.true_branch}, {self.false_branch})"

class CommentNode(StatementNode):
    def __init__(self, content):
        self.content : str = content

    def __repr__(self):
        return f"Comment({self.content})"

class IdentifierNode(Node):
    def __init__(self, value):
        self.value : str = value

    def __repr__(self):
        return f"Identifier({self.value})"

class ExpressionNode(Node):
    pass

class LogicExpressionNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left: ExpressionNode = left
        self.operator : str = operator
        self.right : ExpressionNode = right

    def __repr__(self):
        return f"LogicExpression({self.left}, {self.operator}, {self.right})"

class RelationalExpressionNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left : ExpressionNode = left
        self.operator : str = operator
        self.right : ExpressionNode = right

    def __repr__(self):
        return f"RelationalExpression({self.left}, {self.operator}, {self.right})"

class ArithmeticExpressionNode(ExpressionNode):
    def __init__(self, left, operator=None, right=None):
        self.left : ExpressionNode = left
        self.operator : str = operator
        self.right: ExpressionNode = right

    def __repr__(self):
        return f"ArithmeticExpression({self.left}, {self.operator}, {self.right})"

class TermNode(ExpressionNode):
    def __init__(self, left, operator=None, right=None):
        self.left : ExpressionNode = left
        self.operator : str = operator
        self.right : ExpressionNode = right

    def __repr__(self):
        return f"Term({self.left}, {self.operator}, {self.right})"

class FactorNode(ExpressionNode):
    def __init__(self, value):
        self.value : str = value

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
    
class WhileStatementNode(StatementNode):
    def __init__(self, condition, true_branch):
        self.condition : ExpressionNode = condition
        self.true_branch : StatementNode = true_branch

    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.true_branch})"

# ReturnStatement -> return Expression  | return ;    
class ReturnStatementNode(StatementNode):
    def __init__(self, expression=None):
        self.expression : ExpressionNode = expression

    def __repr__(self):
        return f"ReturnStatement({self.expression})"
    
class BreakStatementNode(StatementNode):
    def __init__(self):
        pass

    def __repr__(self):
        return f"BreakStatement()"

class ContinueStatementNode(StatementNode):
    def __init__(self):
        pass

    def __repr__(self):
        return f"ContinueStatement()"
    
class TypeNode(Node):
    def __init__(self, value):
        self.value : str = value

    def __repr__(self):
        return f"Type({self.value})"
    
###### function      -> func type identifier ( parameters ) { program }
class FunctionNode(Node):
    def __init__(self, type, identifier, parameters, program):
        self.type : TypeNode = type
        self.identifier : IdentifierNode = identifier
        self.parameters : ParametersNode = parameters
        self.program : ProgramNode = program

    def __repr__(self):
        return f"Function({self.type}, {self.identifier}, {self.parameters}, {self.program})"
    
###### parameters    -> type identifier | type identifier , parameters
class ParametersNode(Node):
    def __init__(self, type, identifier, parameters=None):
        self.type : TypeNode = type
        self.identifier : IdentifierNode = identifier
        self.parameters : ParametersNode = parameters

    def __repr__(self):
        return f"Parameters({self.type}, {self.identifier}, {self.parameters})"
    
###### function_call     -> identifier ( parameters )
class FunctionCallNode(Node):
    def __init__(self, identifier, parameters):
        self.identifier : IdentifierNode = identifier
        self.parameters : ParametersNode = parameters

    def __repr__(self):
        return f"FunctionCall({self.identifier}, {self.parameters})"
    
###### function_parameters -> identifier | identifier , function_parameters | ε
class FunctionParametersNode(Node):
    def __init__(self, identifier, parameters=None):
        self.identifier : IdentifierNode = identifier
        self.parameters : FunctionParametersNode = parameters

    def __repr__(self):
        return f"FunctionParameters({self.identifier}, {self.parameters})"
    
###### print     -> print ( expression ) ;
class PrintNode(Node):
    def __init__(self, expression):
        self.expression : ExpressionNode = expression

    def __repr__(self):
        return f"Print({self.expression})"
    
###### special_func  -> print
class SpecialFuncNode(Node):
    def __init__(self, value):
        self.value : str = value

    def __repr__(self):
        return f"SpecialFunc({self.value})"
    
###### initialization -> type identifier = expression | type identifier;
class InitializationNode(Node):
    def __init__(self, type, identifier, expression=None):
        self.type : TypeNode = type
        self.identifier : IdentifierNode = identifier
        self.expression : ExpressionNode = expression

    def __repr__(self):
        return f"Initialization({self.type}, {self.identifier}, {self.expression})"