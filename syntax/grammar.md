# Gramatica de lenguaje 

###### program       -> statement | statement program
###### statement     -> assignment | if_statement | comment
###### assignment    -> identifier = expression ;
###### if_statement  -> if ( expression ) { program } | if ( expression ) { program } else { program }
###### 
###### expression    -> logic_expr | arithmetic_expr
###### logic_expr    -> logic_term | logic_term or logic_expr | logic_term and logic_expr
###### logic_term    -> logic_factor | logic_factor == logic_term | logic_factor != logic_term
###### logic_factor  -> arithmetic_expr | arithmetic_expr < arithmetic_term | arithmetic_expr > arithmetic_term | arithmetic_expr <= arithmetic_term | arithmetic_expr >= arithmetic_term | not logic_expr
###### arithmetic_expr -> term | term + arithmetic_expr | term - arithmetic_expr
###### term          -> factor | factor * term | factor / term
###### factor        -> identifier | number | float_number | string | boolean | ( expression )
###### number        -> [0-9]+
###### float_number  -> [0-9]+.[0-9]+
###### string        -> "[^"]*"
###### boolean       -> true | false
###### identifier    -> [a-zA-Z][a-zA-Z0-9_]*
###### comment       -> //.*\n