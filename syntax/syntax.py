

from typing import List
from lexic.lexic import TokenMatch
from lexic.tokens import Token_dict, Token_enum, Token
from syntax_tree import * 

TOKEN_TYPES_DEF = [
    Token_dict[Token_enum.INTEGER_DEF],
    Token_dict[Token_enum.FLOAT_DEF],
    Token_dict[Token_enum.STRING_DEF],
    Token_dict[Token_enum.BOOL_DEF],
    Token_dict[Token_enum.VOID_DEF]
]
TOKEN_TYPES_VAL = [
    Token_dict[Token_enum.INTEGER_VALUE],
    Token_dict[Token_enum.FLOAT_VALUE],
    Token_dict[Token_enum.STRING_VALUE],
    Token_dict[Token_enum.BOOLEAN_VALUE]
]

class ParserUnexpectedEnd(Exception):
    def __init__(self, index: int , length: int, token: TokenMatch = None):
        self.index = index
        self.length = length
        self.token = token
    def __str__(self):
        if not self.token: 
            return f"unexpected end of input with index {self.index} (tokens length : {self.length})" 
        else:
            return f"unexpected end of input with index {self.index} (tokens length : {self.length})\n{self.token}"
    def __repr__(self):
        return self.__str__()

class ParserUnexpectedType(Exception):
    def __init__(self, expected, acquired):
        self.expected = expected
        self.acquired = acquired 

    def __str__(self):
        return f"expected token {self.expected} but instead got {self.acquired}" 
    def __repr__(self):
        return self.__str__()

class Parser:
    def __init__(self, tokens: List[TokenMatch]):
        self.tokens: List[TokenMatch] = tokens
        self.index: int = 0

    def consume(self, expected_type: TokenMatch =None):
        if self.index >= len(self.tokens):
            raise ParserUnexpectedEnd(self.index, len(self.tokens))
        current_token:Token = self.tokens[self.index]
        if expected_type and current_token.token != expected_type:
            raise ParserUnexpectedType(expected_type, current_token)
        self.index += 1
        return current_token

    def program(self):
        node = ProgramNode()
        while self.index < len(self.tokens):
            if self.tokens[self.index].token == Token_dict[Token_enum.FUNC_END]:
                # if starts with a function end, then is invalid.
                if self.index == 0:
                    raise ParserUnexpectedType("Program started with }", self.tokens[self.index])
                break
            node.children.append(self.statement())

        return node

    ###### statement     -> 
    # special_func | function_def | assignment | initialization |
    # if_statement | while_statement | jump_statement | 
    # function_call ;
    def statement(self):
        if self.tokens[self.index].token in [Token_dict[Token_enum.PRINT]]:
            return self.special_func()
        elif self.tokens[self.index].token == Token_dict[Token_enum.FUNC_DEF]:
            return self.function()
        elif self.tokens[self.index].token in TOKEN_TYPES_DEF:
            return self.initialization()
        elif self.tokens[self.index].token == Token_dict[Token_enum.IDENTIFIER]:
            # function_Call or assignment
            if self.tokens[self.index+1].token == Token_dict[Token_enum.PARAM_START]:
                r = self.function_call()
                ## check if there is a ; at the end
                ## if its out of index, then its an error
                if self.index >= len(self.tokens):
                    raise ParserUnexpectedEnd(self.index, len(self.tokens), self.tokens[self.index-3])
                if self.tokens[self.index].token == Token_dict[Token_enum.END_LINE]:
                    self.consume(Token_dict[Token_enum.END_LINE])
                    return r
            else:
                return self.assignment()

        elif self.tokens[self.index].token == Token_dict[Token_enum.IF]:
            return self.if_statement()
        elif self.tokens[self.index].token == Token_dict[Token_enum.WHILE]:
            return self.while_statement()
        elif self.tokens[self.index].token == Token_dict[Token_enum.RETURN] or self.tokens[self.index].token == Token_dict[Token_enum.BREAK] or self.tokens[self.index].token == Token_dict[Token_enum.CONTINUE]:
            return self.jump_statement()
        else:
            raise ParserUnexpectedType("Invalid statement", self.tokens[self.index])

    def comment(self):
        token = self.consume(Token_dict[Token_enum.COMMENT])
        return CommentNode(token.match)

    ###### while_statement -> while ( expression ) { program }
    def while_statement(self):
        self.consume(Token_dict[Token_enum.WHILE])
        self.consume(Token_dict[Token_enum.PARAM_START])
        condition = self.expression()
        self.consume(Token_dict[Token_enum.PARAM_END])
        self.consume(Token_dict[Token_enum.FUNC_START])
        program = self.program()
        self.consume(Token_dict[Token_enum.FUNC_END])
        return WhileStatementNode(condition, program)

    ###### if_statement  -> if ( expression ) { program } | if ( expression ) { program } else { program }
    def if_statement(self):
        self.consume(Token_dict[Token_enum.IF])
        self.consume(Token_dict[Token_enum.PARAM_START])
        condition = self.expression()
        self.consume(Token_dict[Token_enum.PARAM_END])
        self.consume(Token_dict[Token_enum.FUNC_START])
        true_branch = self.program()
        self.consume(Token_dict[Token_enum.FUNC_END])

        false_branch = None
        if self.index < len(self.tokens) and self.tokens[self.index].token == Token_dict[Token_enum.ELSE]:
            self.consume(Token_dict[Token_enum.ELSE])
            self.consume(Token_dict[Token_enum.FUNC_START])
            false_branch = self.program()
            self.consume(Token_dict[Token_enum.FUNC_END])
        
        return IfStatementNode(condition, true_branch, false_branch)

    ###### jump_statement -> return expression ; | return ; | break ; | continue ;
    def jump_statement(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.RETURN]:
            self.consume(Token_dict[Token_enum.RETURN])
            if self.tokens[self.index].token == Token_dict[Token_enum.END_LINE]:
                self.consume(Token_dict[Token_enum.END_LINE])
                return ReturnStatementNode()
            else:
                expression_node = self.expression()
                self.consume(Token_dict[Token_enum.END_LINE])
                return ReturnStatementNode(expression_node)
        elif self.tokens[self.index].token == Token_dict[Token_enum.BREAK]:
            self.consume(Token_dict[Token_enum.BREAK])
            self.consume(Token_dict[Token_enum.END_LINE])
            return BreakStatementNode()
        elif self.tokens[self.index].token == Token_dict[Token_enum.CONTINUE]:
            self.consume(Token_dict[Token_enum.CONTINUE])
            self.consume(Token_dict[Token_enum.END_LINE])
            return ContinueStatementNode()
        else:
            raise ParserUnexpectedType("Invalid jump statement", self.tokens[self.index])


    ###### initialization -> type identifier = expression | type identifier;
    def initialization(self):
        type_node = self.type()
        identifier_node = self.identifier()
        if self.index < len(self.tokens) and self.tokens[self.index].token == Token_dict[Token_enum.ASSIGN]:
            self.consume(Token_dict[Token_enum.ASSIGN])
            expression_node = self.expression()
            self.consume(Token_dict[Token_enum.END_LINE])
            return InitializationNode(type_node, identifier_node, expression_node)
        else:
            self.consume(Token_dict[Token_enum.END_LINE])
            return InitializationNode(type_node, identifier_node)

    ###### assignment    -> identifier = expression;
    def assignment(self):
        identifier_node = self.identifier()
        self.consume(Token_dict[Token_enum.ASSIGN])
        expression_node = self.expression()
        self.consume(Token_dict[Token_enum.END_LINE])
        return AssignmentNode(identifier_node, expression_node)

    ###### function      -> fun type identifier ( parameters ) { program }
    def function(self):
        self.consume(Token_dict[Token_enum.FUNC_DEF])
        type_node = self.type()
        identifier_node = self.identifier()
        self.consume(Token_dict[Token_enum.PARAM_START])
        parameters_node = self.parameters()
        self.consume(Token_dict[Token_enum.PARAM_END])
        self.consume(Token_dict[Token_enum.FUNC_START])
        program_node = self.program()
        self.consume(Token_dict[Token_enum.FUNC_END])

        return FunctionNode(type_node, identifier_node, parameters_node, program_node)

    ###### function_call     -> identifier ( parameters )
    def function_call(self):
        identifier_node = self.identifier()
        self.consume(Token_dict[Token_enum.PARAM_START])
        parameters_node = self.function_parameters()
        self.consume(Token_dict[Token_enum.PARAM_END])
        return FunctionCallNode(identifier_node, parameters_node)

    ###### function_parameters -> factor | factor , function_parameters | ε
    def function_parameters(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.PARAM_END]:
            return None
        else:
            node = self.factor()
            if self.index < len(self.tokens) and self.tokens[self.index].token == Token_dict[Token_enum.PARAM_SEPARATOR]:
                self.consume(Token_dict[Token_enum.PARAM_SEPARATOR])
                return FunctionParametersNode(node, self.function_parameters())
            else:
                return FunctionParametersNode(node)

    ###### parameters    -> type identifier | type identifier , parameters | ε
    def parameters(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.PARAM_END]:
            return None
        else:
            type_node = self.type()
            identifier_node = self.identifier()
            if self.index < len(self.tokens) and self.tokens[self.index].token == Token_dict[Token_enum.PARAM_SEPARATOR]:
                self.consume(Token_dict[Token_enum.PARAM_SEPARATOR])
                return ParametersNode(type_node, identifier_node, self.parameters())
            else:
                return ParametersNode(type_node, identifier_node)

    ###### special_func  -> print
    def special_func(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.PRINT]:
            return self.print()
        else:
            raise ParserUnexpectedType("Invalid special function", self.tokens[self.index])
    ###### print     -> print ( expression ) ;
    def print(self):
        self.consume(Token_dict[Token_enum.PRINT])
        self.consume(Token_dict[Token_enum.PARAM_START])
        expression_node = self.expression()
        self.consume(Token_dict[Token_enum.PARAM_END])
        self.consume(Token_dict[Token_enum.END_LINE])
        return PrintNode(expression_node)

    ###### type         -> int | float | string | bool | void
    def type(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.INTEGER_DEF]:
            self.consume(Token_dict[Token_enum.INTEGER_DEF])
            return TypeNode("Int")
        elif self.tokens[self.index].token == Token_dict[Token_enum.FLOAT_DEF]:
            self.consume(Token_dict[Token_enum.FLOAT_DEF])
            return TypeNode("Float")
        elif self.tokens[self.index].token == Token_dict[Token_enum.STRING_DEF]:
            self.consume(Token_dict[Token_enum.STRING_DEF])
            return TypeNode("String")
        elif self.tokens[self.index].token == Token_dict[Token_enum.BOOL_DEF]:
            self.consume(Token_dict[Token_enum.BOOL_DEF])
            return TypeNode("Bool")
        elif self.tokens[self.index].token == Token_dict[Token_enum.VOID_DEF]:
            self.consume(Token_dict[Token_enum.VOID_DEF])
            return TypeNode("Void")
        else:
            raise ParserUnexpectedType("Invalid type", self.tokens[self.index])
        
    def identifier(self):
        token = self.consume(Token_dict[Token_enum.IDENTIFIER])
        return IdentifierNode(token.match)

    def expression(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.PARAM_START] \
        or self.tokens[self.index].token == Token_dict[Token_enum.IDENTIFIER]:
            return self.relational_expression()

        elif self.tokens[self.index].token in [Token_dict[Token_enum.AND], Token_dict[Token_enum.OR], Token_dict[Token_enum.NOT]]:
            return self.logic_expression()

        else:
            return self.arithmetic_expression()
        
    def logic_expression(self):
        node = self.relational_expression()
        while self.index < len(self.tokens) and self.tokens[self.index].token in [Token_dict[Token_enum.AND], Token_dict[Token_enum.OR]]:
            if self.tokens[self.index].token == Token_dict[Token_enum.AND]:
                operator = "and"
                self.consume(Token_dict[Token_enum.AND])
            else:
                operator = "or"
                self.consume(Token_dict[Token_enum.OR])
            node = LogicExpressionNode(node, operator, self.relational_expression())
        return node

    def relational_expression(self):
        node = self.arithmetic_expression()
        while self.index < len(self.tokens) and self.tokens[self.index].token in [Token_dict[Token_enum.EQUAL], Token_dict[Token_enum.NOT_EQUAL], Token_dict[Token_enum.GREATER], Token_dict[Token_enum.LESS], Token_dict[Token_enum.GREATER_EQUAL], Token_dict[Token_enum.LESS_EQUAL]]:
            if self.tokens[self.index].token == Token_dict[Token_enum.EQUAL]:
                operator = "=="
                self.consume(Token_dict[Token_enum.EQUAL])
            elif self.tokens[self.index].token == Token_dict[Token_enum.NOT_EQUAL]:
                operator = "!="
                self.consume(Token_dict[Token_enum.NOT_EQUAL])
            elif self.tokens[self.index].token == Token_dict[Token_enum.GREATER]:
                operator = ">"
                self.consume(Token_dict[Token_enum.GREATER])
            elif self.tokens[self.index].token == Token_dict[Token_enum.LESS]:
                operator = "<"
                self.consume(Token_dict[Token_enum.LESS])
            elif self.tokens[self.index].token == Token_dict[Token_enum.GREATER_EQUAL]:
                operator = ">="
                self.consume(Token_dict[Token_enum.GREATER_EQUAL])
            else:
                operator = "<="
                self.consume(Token_dict[Token_enum.LESS_EQUAL])
            node = RelationalExpressionNode(node, operator, self.arithmetic_expression())
        return node

    def arithmetic_expression(self):
        node = self.term()
        while self.index < len(self.tokens) and self.tokens[self.index].token in [Token_dict[Token_enum.SUM], Token_dict[Token_enum.SUB]]:
            if self.tokens[self.index].token == Token_dict[Token_enum.SUM]:
                operator = "+"
                self.consume(Token_dict[Token_enum.SUM])
            else:
                operator = "-"
                self.consume(Token_dict[Token_enum.SUB])
            node = ArithmeticExpressionNode(node, operator, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.index < len(self.tokens) and self.tokens[self.index].token in [Token_dict[Token_enum.MULT], Token_dict[Token_enum.DIV]]:
            if self.tokens[self.index].token == Token_dict[Token_enum.MULT]:
                operator = "*"
                self.consume(Token_dict[Token_enum.MULT])
            else:
                operator = "/"
                self.consume(Token_dict[Token_enum.DIV])
            node = TermNode(node, operator, self.factor())
        return node

    ###### factor        -> identifier | number | float_number | string | boolean | ( expression ) | function_call
    def factor(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.PARAM_START]:
            self.consume(Token_dict[Token_enum.PARAM_START])
            node = self.expression()
            self.consume(Token_dict[Token_enum.PARAM_END])
            return FactorNode(node)
        elif self.tokens[self.index].token == Token_dict[Token_enum.INTEGER_VALUE]:
            token = self.consume(Token_dict[Token_enum.INTEGER_VALUE])
            return FactorNode(IntNode(token.match))
        elif self.tokens[self.index].token == Token_dict[Token_enum.FLOAT_VALUE]:
            token = self.consume(Token_dict[Token_enum.FLOAT_VALUE])
            return FactorNode(FloatNode(token.match))
        elif self.tokens[self.index].token == Token_dict[Token_enum.STRING_VALUE]:
            token = self.consume(Token_dict[Token_enum.STRING_VALUE])
            return FactorNode(StringNode(token.match))
        elif self.tokens[self.index].token == Token_dict[Token_enum.BOOLEAN_VALUE]:
            token = self.consume(Token_dict[Token_enum.BOOLEAN_VALUE])
            return FactorNode(BooleanNode(token.match))
        else:
            if self.tokens[self.index+1].token == Token_dict[Token_enum.PARAM_START]:
                return self.function_call()
            return FactorNode(self.identifier())

    def parse(self):
        return self.program()


def parse_program(tokens : List[TokenMatch]):
    parser = Parser(tokens)
    return parser.parse()