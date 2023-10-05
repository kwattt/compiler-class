
from lexic import lexic_analyzer
from syntax import parse_program, view_tree
#from syntax import parse_program, view_tree
sample_code = """
if((a<c)>b){
    c=1;
}
"""

# Parsing the sample code
print(sample_code)
tokens = lexic_analyzer(sample_code)
#print(tokens)
parsed_tree = parse_program(tokens)
print(parsed_tree)
view_tree(sample_code, parsed_tree)