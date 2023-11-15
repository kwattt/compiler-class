from lexic import lexic_analyzer
from semantic import *
from syntax import parse_program

example_code = open("example_code.txt", "r").read()
## add number to each line
new_matches = lexic_analyzer(example_code)
example_code = '\n'.join([f"{number} {line}" for number, line in enumerate(example_code.split('\n'))])
tree = parse_program(new_matches)

data = SemanticAnalyzer(tree).analyze()
