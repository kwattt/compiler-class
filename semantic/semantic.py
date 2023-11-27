from syntax import * 

class SemanticError(Exception):
    pass

class Table: 
    def __init__(self) -> None:
        self.table = {}

    def add(self, name, type, isdef, isfunc):
        if not name in self.table:
            self.table[name] = [[type, isdef, isfunc]]
        else:
            self.table[name].append([type, isdef, isfunc])

    def get(self, name):
        if name in self.table:
            return self.table[name]
        else:
            return None

    def getall(self):
        return self.table

class SemanticAnalyzer:
    def __init__(self, program_node):
        self.program_node = program_node
        self.symbol_table = Table()

    def analyze(self):
        self.visit(self.program_node)
        print(self.symbol_table.getall())
        return self.symbol_table.getall()

    def visit(self, node):
        # Dispatch to the specific visit method based on node type
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Visit each child of the node
        for attribute in vars(node).values():
            if isinstance(attribute, list):
                for item in attribute:
                    if isinstance(item, Node):
                        self.visit(item)
            elif isinstance(attribute, Node):
                self.visit(attribute)

    def visit_FactorNode(self, node):
        return node.value.__class__
    
    def visit_ExpressionNode(self, node):
        return node.value.__class__

    def visit_InitializationNode(self, node):
        # Corrected to use 'node.identifier.value'
        #if node.identifier.value in self.symbol_table:
        if self.symbol_table.get(node.identifier.value) != None:
            raise SemanticError(f"Variable '{node.identifier.value}' is already defined")
        self.symbol_table.add(node.identifier.value, node.type, 1, 0)
        # If the variable is initialized, check the expression's type
        if node.expression:
            expr_type = node.expression.value.__class__.__name__
            if str(expr_type) != str(node.type):
                raise SemanticError(f"Type mismatch in initialization of '{node.identifier.value}' - expected {node.type} got {expr_type}")

    def parse_parameters(self, parameters: ParametersNode):
        if parameters.parameters: 
            self.parse_parameters(parameters.parameters)
        if self.symbol_table.get(parameters.identifier.value) != None:
            raise SemanticError(f"Variable '{parameters.identifier.value}' is already defined")
        else :
            self.symbol_table.add(parameters.identifier.value, parameters.type, 0, 0)

    def visit_FunctionNode(self, node):
        function_name = node.identifier.value
        #if function_name in self.symbol_table:
        if self.symbol_table.get(function_name) != None:
            raise SemanticError(f"Function '{function_name}' is already defined")
        #self.symbol_table[function_name] = [node.type, 1, 0]
        self.symbol_table.add(function_name, node.type, 1, 1)

        if node.parameters:
            self.parse_parameters(node.parameters)
                
        self.visit(node.program)

    def visit_FunctionCallNode(self, node):
        if self.symbol_table.get(node.identifier.value) == None:
            raise SemanticError(f"Function '{node.identifier.value}' is not defined")
        
        if self.symbol_table.get(node.identifier.value)[0][2] != 1:
            raise SemanticError(f"'{node.identifier.value}' is not a function")

        if node.parameters:
            if self.visit(node.parameters) != self.symbol_table.get(node.identifier.value)[0][0]:
                raise SemanticError(f"Type mismatch in function call to '{node.identifier.value}'")
            
        self.symbol_table.add(node.identifier.value, self.symbol_table.get(node.identifier.value)[0][0], 0, 1)

    def visit_AssignmentNode(self, node):
        #if node.identifier.value not in self.symbol_table:
        if self.symbol_table.get(node.identifier.value) == None:
            raise SemanticError(f"Variable '{node.identifier.value}' is used before assignment")
        var_type = self.symbol_table.get(node.identifier.value)[0][0]

        if isinstance(node.expression, ArithmeticExpressionNode):
            if node.expression.left.value.__class__.__name__ != node.expression.right.value.__class__.__name__:
                raise SemanticError(f"1Type mismatch in assignment to '{node.identifier.value}', {node.expression.left.value.__class__.__name__} and {node.expression.right.value.__class__.__name__}")
            ## check if types are the same
            elif node.expression.left.value.__class__.__name__ != str(var_type):
                raise SemanticError(f"2Type mismatch in assignment to {node.identifier.value}, {node.expression.left.value.__class__.__name__} and {str(var_type)}")
            elif node.expression.right.value.__class__.__name__ != str(var_type):
                raise SemanticError(f"3Type mismatch in assignment to {node.identifier.value}, {node.expression.left.value.__class__.__name__} and {str(var_type)}")

        elif node.expression.value.__class__.__name__ != str(var_type):
            ## is assigning to a variable? 
            ## lets check if variable is already defined
            if self.symbol_table.get(node.expression.value.value) == None:
                # check if its variable or is another kind of expression
                if node.expression.value.__class__.__name__ == "IdentifierNode":
                    raise SemanticError(f"4Variable '{node.expression.value.value}' is not defined")
                else:
                    ## lets check that type is the same as the variable type
                    if node.expression.value.__class__.__name__ != self.symbol_table.get(node.identifier.value)[0][0]:
                        raise SemanticError(f"5Type mismatch in assignment to '{node.identifier.value}', {node.expression.value.__class__.__name__} and {str(var_type)}")

            ## lest check if types are the same
            elif str(self.symbol_table.get(node.expression.value.value)[0][0]) != str(var_type):
                raise SemanticError(f"6Type mismatch in assignment to '{node.identifier.value}', {self.symbol_table.get(node.expression.value.value)[0][0]} and {str(var_type)}")
            

    def visit_IdentifierNode(self, node):
        #if node.value not in self.symbol_table:
        #    print(self.symbol_table)
        if self.symbol_table.get(node.value) == None:
            raise SemanticError(f"Variable '{node.value}' is not defined")
        return self.symbol_table.get(node.value)[0][0]