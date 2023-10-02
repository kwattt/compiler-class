# Gramatica de lenguaje 

#### program  -> assignment | assignment program
#### assignment -> identifier = expression ;
#### identifier   -> [a-zA-Z][a-zA-Z0-9_]*
#### expression -> term> | term + expression | term - expression
#### term       -> factor | factor * term | factor / term
#### factor     -> identifier | number | ( expression )
#### number     -> [0-9]+
