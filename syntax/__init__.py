import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from syntax.syntax import parse_program, ParserUnexpectedEnd, ParserUnexpectedType
from syntax_tree import *