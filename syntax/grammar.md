# Gramatica de lenguaje 

##### Keywords 
###### if, else, while, break, true, false, or, and, not
###### int, float, string, bool, void
###### return, break, continue
###### func 
###### program       -> statement 
###### statement     -> special_func | function_def | assignment | if_statement | while_statement | comment | jump_statement | function_call ;
###### initialization -> type identifier = expression | type identifier;
###### assignment    -> identifier = expression;
###### if_statement  -> if ( expression ) { program } | if ( expression ) { program } else { program }
###### 
###### jump_statement -> return expression ; | return | break ; | continue ;
###### expression    -> logic_expr | arithmetic_expr
###### logic_expr    -> logic_term | logic_term or logic_expr | logic_term and logic_expr
###### logic_term    -> logic_factor | logic_factor == logic_term | logic_factor != logic_term
###### logic_factor  -> arithmetic_expr | arithmetic_expr < arithmetic_term | arithmetic_expr > arithmetic_term | arithmetic_expr <= arithmetic_term | arithmetic_expr >= arithmetic_term | not logic_expr
###### arithmetic_expr -> term | term + arithmetic_expr | term - arithmetic_expr
###### term          -> factor | factor * term | factor / term
###### type         -> int | float | string | bool | void
###### factor        -> identifier | number | float_number | string | boolean | ( expression ) | function_call
###### number        -> [0-9]+
###### float_number  -> [0-9]+.[0-9]+
###### string        -> "[^"]*"
###### boolean       -> true | false
###### identifier    -> [a-zA-Z][a-zA-Z0-9_]*
###### comment       -> //.*\n
###### while_statement -> while ( expression ) { program }
###### function_def      -> fun type identifier ( parameters ) { program }
###### function_call     -> identifier ( parameters ) 
###### parameters    -> type identifier | type identifier , parameters |  ε
###### function_parameters -> factor | factor , function_parameters |  ε

###### cin -> cin >> identifier ;

##### Special funcs
###### special_func  -> print
###### print     -> print ( expression ) ;