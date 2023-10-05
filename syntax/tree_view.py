
## lets create a tree view of the parsed tree
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from syntax_tree import *

# Function to insert nodes into the treeview
tree = None 
program_node = None
def tree_view(code, program_nodex):
    global tree 
    global program_node
    program_node = program_nodex

    root = tk.Tk()
    root.title("Syntax Tree Visualizer")

    # Create input Text widget
    text_input = tk.Text(root, height=10, width=40)
    text_input.pack(pady=10)
    text_input.insert(tk.END, code)

    # Create parse button
    btn_parse = tk.Button(root, text="Parse and Visualize", command=parse_and_visualize)
    btn_parse.pack(pady=10)

    # Create treeview for the syntax tree
    tree = ttk.Treeview(root)
    tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)

    root.mainloop()

def insert_node(tree, parent, node):
    print("inserting", parent, node, type(node))
    if isinstance(node, ProgramNode):
        id = tree.insert(parent, "end", text="Program")
        for child in node.children:
            insert_node(tree, id, child)
    elif isinstance(node, AssignmentNode):
        print("assigment", node, node.expression)
        id = tree.insert(parent, "end", text=f"Assignment to {node.identifier.value}")
        insert_node(tree, id, node.expression)
    elif isinstance(node, IdentifierNode):
        tree.insert(parent, "end", text=f"Identifier: {node.value}")
    elif isinstance(node, ArithmeticExpressionNode):
        id = tree.insert(parent, "end", text=f"Arithmetic Expression ({node.operator})")
        insert_node(tree, id, node.left)
        if node.right: insert_node(tree, id, node.right)    
        elif isinstance(node, NumberNode):
            tree.insert(parent, "end", text=f"Number: {node.value}")    
    
    elif isinstance(node, AssignmentNode):
        id = tree.insert(parent, "end", text=f"Assignment to {node.identifier.value}")
        insert_node(tree, id, node.expression)

    elif isinstance(node, IdentifierNode):
        tree.insert(parent, "end", text=f"Identifier: {node.value}")

    elif isinstance(node, ArithmeticExpressionNode):
        id = tree.insert(parent, "end", text=f"Arithmetic Expression ({node.operator})")
        insert_node(tree, id, node.left)
        if node.right:
            if node.right: insert_node(tree, id, node.right)
    
        insert_node(tree, id, node.left)
        if node.right:
            if node.right: insert_node(tree, id, node.right)

    elif isinstance(node, FactorNode):
        if isinstance(node, NumberNode):
            tree.insert(parent, "end", text=f"Number: {node.value}")
        elif isinstance(node, FloatNode):
            tree.insert(parent, "end", text=f"Float: {node.value}")
        elif isinstance(node, StringNode):
            tree.insert(parent, "end", text=f"String: {node.value}")
        elif isinstance(node, BooleanNode):
            tree.insert(parent, "end", text=f"Boolean: {node.value}")
        else:
            tree.insert(parent, "end", text=f"Factor: {node.value}")
    elif isinstance(node, IfStatementNode):
        id = tree.insert(parent, "end", text="If Statement")
        insert_node(tree, id, node.condition)
        insert_node(tree, id, node.true_branch)
        if node.false_branch:
            insert_node(tree, id, node.false_branch)

    elif isinstance(node, CommentNode):
        tree.insert(parent, "end", text=f"Comment: {node.content}")

    elif isinstance(node, LogicExpressionNode):
        id = tree.insert(parent, "end", text=f"Logic Expression ({node.operator})")
        insert_node(tree, id, node.left)
        if node.right: insert_node(tree, id, node.right)

    elif isinstance(node, RelationalExpressionNode):
        id = tree.insert(parent, "end", text=f"Relational Expression ({node.operator})")
        insert_node(tree, id, node.left)
        if node.right: insert_node(tree, id, node.right)

    elif isinstance(node, FloatNode):
        tree.insert(parent, "end", text=f"Float: {node.value}")
    elif isinstance(node, StringNode):
        tree.insert(parent, "end", text=f"String: {node.value}")
    elif isinstance(node, BooleanNode):
        tree.insert(parent, "end", text=f"Boolean: {node.value}")
# Function to handle the parse and visualize button
def parse_and_visualize():
    global tree 
    global program_node
    tree.delete(*tree.get_children())
    try:
        insert_node(tree, "", program_node)
    except Exception as e:
        messagebox.showerror("Error", str(e))

