

from typing import List
from lexic.lexic import TokenMatch
from lexic.tokens import Token_dict, Token_enum, Token
from syntax_tree import * 

class ParserUnexpectedEnd(Exception):
    def __init__(self, index: int , length: int):
        self.index = index
        self.length = length

    def __str__(self):
        return f"unexpected end of input with index {self.index} (tokens length : {self.length})" 
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
            raise ParserUnexpectedType(expected_type, current_token.token)
        self.index += 1
        return current_token

    def program(self):
        node = ProgramNode()
        while self.index < len(self.tokens):
            if self.tokens[self.index].token == Token_dict[Token_enum.IF]:
                node.children.append(self.if_statement())
            elif self.tokens[self.index].token == Token_dict[Token_enum.IDENTIFIER]:
                node.children.append(self.statement())
            ## check if its } or end of file
            elif self.tokens[self.index].token == Token_dict[Token_enum.FUNC_END]:
                break

        return node

    def statement(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.COMMENT]:
            return self.comment()
        else:
            return self.assignment()

    def comment(self):
        token = self.consume(Token_dict[Token_enum.COMMENT])
        return CommentNode(token.match)

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

    def assignment(self):
        identifier = self.identifier()
        self.consume(Token_dict[Token_enum.ASSIGN])
        expression = self.expression()
        self.consume(Token_dict[Token_enum.END_LINE])
        return AssignmentNode(identifier, expression)

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

    def factor(self):
        if self.tokens[self.index].token == Token_dict[Token_enum.PARAM_START]:
            self.consume(Token_dict[Token_enum.PARAM_START])
            node = self.expression()
            self.consume(Token_dict[Token_enum.PARAM_END])
            return FactorNode(node)
        elif self.tokens[self.index].token == Token_dict[Token_enum.INTEGER_VALUE]:
            token = self.consume(Token_dict[Token_enum.INTEGER_VALUE])
            return FactorNode(NumberNode(token.match))
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
            return FactorNode(self.identifier())

    def parse(self):
        return self.program()


def parse_program(tokens : List[TokenMatch]):
    parser = Parser(tokens)
    return parser.parse()