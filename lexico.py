import re 
from enum import Enum
# typings
from typing import List, Tuple
from tokens import Token_enum, Token_dict, Token

## regex valid language with A-Z, a-z 0-9, _

class TokenMatch:
    def __init__(self, token: Token, span: Tuple[int, int], line: int, match: str):
        self.token = token
        self.span = span
        self.line = line
        self.match = match

    def __str__(self):
        return f"linea: {self.line}  pos: {self.span}  token: {self.token.comentary}  match: {self.match}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.token == other.token and self.span == other.span and self.line == other.line and self.match == other.match

class InvalidTokenException(Exception):
    def __init__(self, match: TokenMatch):
        self.match = match

    def __str__(self):
        return f"invalid token {self.match.match} at line {self.match.line}, pos {self.match.span[0]-1}"
    
    def __repr__(self):
        return self.__str__()
    
def parse_code(code) -> List[TokenMatch]:
    matches: List[TokenMatch] = []

    ## first remove comments from the code. we find the special token for comments, and remove the string after it
    token_comment = Token_dict[Token_enum.COMMENT]
    ncode = ''
    for line in code.split('\n'):
        for match in re.finditer(token_comment.identifiers[0], line):
            line = line[:match.span()[0]]
        ncode += line + '\n'
    code = ncode

    ## find all valid tokens
    for number, line in enumerate(code.split('\n')):
        for token in Token_dict.values():
            for identifier in token.identifiers:
                for match in re.finditer(identifier, line):
                    #print(match.group(), token.comentary, number, match.span(), f"  [[[ {line[match.span()[0]:match.span()[1]]} ]]]")
                    #matches.append((token, match.span(), number, line[match.span()[0]:match.span()[1]]))
                    matches.append(TokenMatch(token, match.span(), number, line[match.span()[0]:match.span()[1]]))
                    ## if its invalid print it 
                    if token == Token_dict[Token_enum.INVALID_IDENTIFIER]:
                        print(f"invalid token {match.group()} at line {number}, pos {match.span()[0]-1}")
                        
    # check for repeated matches, IE: // is a comment but contains div token, so we need to remove the div token, and keep the comment token
    # this is done by checking if the match is contained in another match pos and same line, if it is not, we add to the new list
    new_matches = matches
    for match in matches:
        for match2 in matches: 
            if match2 != match and match.line == match2.line: ## tokens in the same line
                if match2.match in match.match:
                    ## lives in the same space as another token
                    if match.span[0] <= match2.span[0] and match.span[1] >= match2.span[1]:
                        #print("removing",match2.match, match.match)

                        # if match2 is an identifier, make sure it is not any other token, for example
                        # void could be an identifier, but it is also a token, so we need to make sure it is not a token
                        if match.token == Token_dict[Token_enum.IDENTIFIER]:
                            # check if it is a token
                            #print(match2.match, "is a toking", match.match)
                            is_token = False
                            for token in Token_dict.values():
                                if match2.match in token.identifiers:
                                    for identifier in token.identifiers:
                                        if len(identifier) == len(match.match):
                                            is_token = True
                                            #print(match2.match, match.match, "is being saved.. its a token")
                                            break

                            if is_token:
                                #print("saving..", match2.match, match.match)
                                continue
                            #print(match2.match, match.match, "is dead")
                        #print("removed", match2)
                        ## .remove is not working because it removes the first match, not the one we are iterating
                        lnew = []
                        for x in new_matches:
                            if x != match2:
                                lnew.append(x)
                            #else: 
                            #    print("found the bitch", match2, x.match)

                        new_matches = [x for x in new_matches if x != match2]

    # order by line and span
    new_matches = sorted(new_matches, key=lambda x: (x.line, x.span[0]))

    for match in new_matches:    
        if match.token == Token_dict[Token_enum.INVALID_IDENTIFIER]:
            raise InvalidTokenException(match)
        
    ## find symbols that were not classified, remove brute tokens from code string

    ncode = code.split('\n')
    for match in new_matches:
        # replace span range with spaces in code 
        line = list(ncode[match.line])
        for char in range(match.span[0], match.span[1]):

            line[char] = ' '

        ncode[match.line] = ''.join(line)

    invalid_words = []
    for i, line in enumerate(ncode):
        invalid_start = -1
        invalid = ''
        for pos,char in enumerate(line): 
            if char not in [' ', '\t', '\r', '\n']:
                if pos == invalid_start+1:
                    invalid_start = pos 
                    invalid += char
                else:
                    invalid_start = pos 
                    invalid = char

        if invalid_start != -1:
            invalid_words.append(
                TokenMatch(Token_dict[Token_enum.INVALID_IDENTIFIER], (invalid_start+1, invalid_start+len(invalid)+1), i, invalid)
            )
    
    for match in invalid_words:
        if match.token == Token_dict[Token_enum.INVALID_IDENTIFIER]:
            raise InvalidTokenException(match)

    return new_matches
## exception type for invalid tokens, use Match to get info 
