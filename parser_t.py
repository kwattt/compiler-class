
from lexic import lexic_analyzer
from syntax import parse_program
from syntax import program_to_tree

sample_code = """
int a; 
cin = a;
int b;
cin = b;
int c;
c = a + b;
print(c);
"""

tokens = lexic_analyzer(sample_code)
parsed_tree = parse_program(tokens)
tree = program_to_tree(parsed_tree)

def pretty_print_dict(d, indent=0):
    res = ""
    for k, v in d.items():
        res += " "*indent + str(k) + "\n"
        if isinstance(v, dict):
            res += pretty_print_dict(v, indent+1)
        else:
            # if its a list 
            if isinstance(v, list):
                for i in v:
                    if isinstance(i, dict):
                        res += pretty_print_dict(i, indent+1)
                    else:
                        res += " "*(indent+1) + str(i) + "\n"
            else:
                res += " "*(indent+1) + str(v) + "\n"
    return res

#print(tree)
print(pretty_print_dict(tree))

# print the tree