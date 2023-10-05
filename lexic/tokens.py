from enum import Enum
from typing import List

class Token:
    def __init__(self, identifiers: List[str], comentary: str):
        self.identifiers = identifiers
        self.comentary = comentary

    def __str__(self):
        return f"Token: {self.identifiers} {self.comentary}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.identifiers == other.identifiers and self.comentary == other.comentary
    
    def __hash__(self):
        return hash((tuple(self.identifiers), self.comentary))

class Token_enum(Enum):
    INTEGER_DEF = 1
    FLOAT_DEF = 2
    STRING_DEF = 3
    VOID_DEF = 4
    BOOL_DEF = 5

    PARAM_START = 6
    PARAM_END = 7
    FUNC_START = 8
    FUNC_END = 9
    RETURN = 10
    END_LINE = 11
    INTEGER_VALUE = 12
    STRING_VALUE = 13
    FLOAT_VALUE = 14

    PRINT = 15
    SUM = 16
    SUB = 17
    DIV = 18
    MULT = 19
    MOD = 20
    ASSIGN = 21
    EQUAL = 22
    NOT_EQUAL = 23
    GREATER = 24
    LESS = 25
    GREATER_EQUAL = 26
    LESS_EQUAL = 27
    AND = 28
    OR = 29
    NOT = 30
    IF = 31
    ELSE = 32
    WHILE = 33
    FOR = 34
    BREAK = 35
    CONTINUE = 36

    BOOLEAN_VALUE = 37

    COMMENT = 38

    IDENTIFIER = 39
    INVALID_IDENTIFIER = 40
    #TOKEN_EOF = 41

Token_dict = {
    Token_enum.INTEGER_DEF: Token(["int"], "definicion de entero"), # init int
    Token_enum.FLOAT_DEF: Token(["float"], "definicion de float"), # init float
    Token_enum.STRING_DEF: Token(["string"], "definicion de string"), # init string
    Token_enum.VOID_DEF: Token(["void"], "definicion de void"), # init void
    Token_enum.BOOL_DEF: Token(["bool"], "definicion de booleano"), # init bool

    Token_enum.PARAM_START: Token([r"\("], "inicio de parametros"), # paramenter start
    Token_enum.PARAM_END: Token([r"\)"], "fin de parametros"), # parameter end

    Token_enum.FUNC_START: Token(["{"], "inicio de funcion"), # func start
    Token_enum.FUNC_END: Token(["}"], "final de funcion"), # func end
    Token_enum.RETURN: Token(["return"], "retorno de funcion"), # return func
    Token_enum.END_LINE: Token([";"], "fin de linea"), # end func

    Token_enum.INTEGER_VALUE: Token([r"\d+"], "numero entero"), # number
    Token_enum.STRING_VALUE: Token([r'".*"', r"'.*'"], "string"), # string
    Token_enum.FLOAT_VALUE: Token([r'[+-]?(?=\d*[.eE])(?=\.?\d)\d*\.?\d*(?:[eE][+-]?\d+)?'], "numero flotante"), # float
    
    Token_enum.PRINT: Token(["print"], "print func"),
    Token_enum.SUM: Token(["\+"], 'suma'),
    Token_enum.SUB: Token(["-"], 'resta'),
    Token_enum.DIV: Token(["/"], 'division'),
    Token_enum.MULT: Token(["\*"], 'multiplicacion'),
    Token_enum.MOD: Token(["%"], 'modulo'),

    Token_enum.ASSIGN: Token(["="], 'asignacion'),
    Token_enum.EQUAL: Token(["=="], 'igualdad'),

    Token_enum.NOT_EQUAL: Token(["!="], 'desigualdad'),
    Token_enum.GREATER: Token([">"], 'mayor'),
    Token_enum.LESS: Token(["<"], 'menor'),
    Token_enum.GREATER_EQUAL: Token([">="], 'mayor o igual'),
    Token_enum.LESS_EQUAL: Token(["<="], 'menor o igual'),
    Token_enum.AND: Token(["&&", "and"], 'and'),
    Token_enum.OR: Token(["\|\|", "or"], 'or'),
    Token_enum.NOT: Token(["!", "not"], 'not'),

    Token_enum.IF: Token(["if"], 'if'),
    Token_enum.ELSE: Token(["else"], 'else'),
    Token_enum.WHILE: Token(["while"], 'while'),
    Token_enum.FOR: Token(["for"], 'for'),
    Token_enum.BREAK: Token(["break"], 'break'),
    Token_enum.CONTINUE: Token(["continue"], 'continue'),

    Token_enum.BOOLEAN_VALUE: Token(["false","true"], 'booleano'),

    Token_enum.COMMENT: Token(["//"], 'comentario'),

    # Identifier, ej function names, variable names
    # basically any word that doesnt start with a number, and is not a reserved word
    Token_enum.IDENTIFIER: Token([r'(?<![\w#?])[a-zA-Z]+[0-9]*(?![\w#?])'], 'identificador'),
    ## invalid identifier,basically the before regex inverted
    Token_enum.INVALID_IDENTIFIER: Token([r"\b[0-9]+[a-zA-Z_]+\b"], 'identificador invalido'),
    #Token_enum.TOKEN_EOF: Token([""], 'fin de archivo')
}