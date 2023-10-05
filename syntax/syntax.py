

from typing import List
from lexic.lexic import TokenMatch
from lexic.tokens import Token_dict, Token_enum, Token
from token_map import * 

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
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.index: int = 0

    def consume(self, expected_type: Token =None):
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
            node.children.append(self.assignment())
        return node

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
        node = self.term()
        while self.index < len(self.tokens) and self.tokens[self.index].token in [Token_dict[Token_enum.SUM], Token_dict[Token_enum.SUB]]:
            if self.tokens[self.index].token == Token_dict[Token_enum.SUM]:
                self.consume(Token_dict[Token_enum.SUM])
                operator = "+"
            else:
                self.consume(Token_dict[Token_enum.SUB])
                operator = "-"
            node = ExpressionNode(node, operator, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.index < len(self.tokens) and self.tokens[self.index].token in [Token_dict[Token_enum.MULT], Token_dict[Token_enum.DIV]]:
            if self.tokens[self.index].token == Token_dict[Token_enum.MULT]:
                self.consume(Token_dict[Token_enum.MULT])
                operator = "*"
            else:
                self.consume(Token_dict[Token_enum.DIV])
                operator = "/"
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
        else:
            return FactorNode(self.identifier())

    def parse(self):
        return self.program()

def parse_program(tokens : List[TokenMatch]):
    parser = Parser(tokens)
    return parser.parse()