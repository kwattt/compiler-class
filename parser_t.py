from lexico.lexico import lexic_analyzer
from lexico.tokens import Token_dict, Token_enum
from token_map import AssignmentNode, ExpressionNode, FactorNode, IdentifierNode, NumberNode, ProgramNode, TermNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def consume(self, expected_type=None):
        if self.index >= len(self.tokens):
            raise Exception("Unexpected end of input")
        current_token = self.tokens[self.index]
        if expected_type and current_token.token != expected_type:
            raise Exception(f"Expected {expected_type} but got {current_token.token}")
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


def parse_program(code):
    tokens = lexic_analyzer(code)
    parser = Parser(tokens)
    return parser.parse()


sample_code = """
x = (y+z);
"""

# Parsing the sample code
parsed_tree = parse_program(sample_code)
print(parsed_tree)
