from lexico import parse_code, Token_enum, Token_dict, InvalidTokenException

# read file example_code.txt

example_code = open("example_code.txt", "r").read()
## add number to each line
new_matches = parse_code(example_code)
example_code = '\n'.join([f"{number} {line}" for number, line in enumerate(example_code.split('\n'))])

processed_text = ''
print("==matches==")
for match in new_matches:
    #print(match)

    processed_text += match.match + ' '
print("Texto procesado:\n====================")
print(processed_text)