
## lets create a tree view of the parsed tree
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from parser_t import parse_program
from token_map import AssignmentNode, ExpressionNode, FactorNode, IdentifierNode, NumberNode, ProgramNode, TermNode

# Function to insert nodes into the treeview
def insert_node(tree, parent, node):
    if isinstance(node, ProgramNode):
        id = tree.insert(parent, "end", text="Program")
        for child in node.children:
            insert_node(tree, id, child)
    elif isinstance(node, AssignmentNode):
        id = tree.insert(parent, "end", text=f"Assignment to {node.identifier.value}")
        insert_node(tree, id, node.expression)
    elif isinstance(node, IdentifierNode):
        tree.insert(parent, "end", text=f"Identifier: {node.value}")
    elif isinstance(node, ExpressionNode):
        id = tree.insert(parent, "end", text=f"Expression ({node.operator})")
        insert_node(tree, id, node.left)
        insert_node(tree, id, node.right)
    elif isinstance(node, TermNode):
        id = tree.insert(parent, "end", text=f"Term ({node.operator})")
        insert_node(tree, id, node.left)
        insert_node(tree, id, node.right)
    elif isinstance(node, FactorNode):
        id = tree.insert(parent, "end", text="Factor")
        insert_node(tree, id, node.value)
    elif isinstance(node, NumberNode):
        tree.insert(parent, "end", text=f"Number: {node.value}")

# Function to handle the parse and visualize button
def parse_and_visualize():
    code = text_input.get("1.0", tk.END)
    tree.delete(*tree.get_children())
    try:
        parsed_tree = parse_program(code)
        insert_node(tree, "", parsed_tree)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Syntax Tree Visualizer")

sample_code = """
x = 5;
jalisco = x + 10;
z = x * y + 2;
x = x * z;
"""

# Create input Text widget
text_input = tk.Text(root, height=10, width=40)
text_input.pack(pady=10)
text_input.insert(tk.END, sample_code)

# Create parse button
btn_parse = tk.Button(root, text="Parse and Visualize", command=parse_and_visualize)
btn_parse.pack(pady=10)

# Create treeview for the syntax tree
tree = ttk.Treeview(root)
tree.pack(pady=20, padx=10, expand=True, fill=tk.BOTH)

root.mainloop()