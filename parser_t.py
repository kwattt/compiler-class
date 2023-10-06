
from lexic import lexic_analyzer
from syntax import parse_program
from syntax import program_to_tree

sample_code = """
int integral = 2;
while (true) {
    if (a==false){
        break;
        }
}
// buenas tardes..

int asd = 22;

fun int suma(int a, int b) {
    return a+b;
}

int i = 22;
if((2+2)==4) {
    print("verdad");
    void a = 0;
    print(suma(2,3));
} else {
    print("you suck");
}
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