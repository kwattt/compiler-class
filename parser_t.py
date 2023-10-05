
from lexic import lexic_analyzer
from syntax import parse_program, view_tree
sample_code = """
x = 22;
y = 3+3;
z = x+y;
z = z*z/y;
"""

# Parsing the sample code
print(sample_code)
tokens = lexic_analyzer(sample_code)
parsed_tree = parse_program(tokens)
print(parsed_tree)
view_tree(sample_code, parsed_tree)