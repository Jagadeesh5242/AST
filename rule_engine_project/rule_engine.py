import ast

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }

def create_rule(rule_string):
    # Parse the rule_string into an AST
    try:
        node = ast.parse(rule_string, mode='eval')
        return convert_ast_node(node.body)
    except SyntaxError as e:
        raise ValueError(f"Invalid rule string: {e}")

def convert_ast_node(node):
    """ Convert ast.AST to a Node. """
    if isinstance(node, ast.BoolOp):
        return Node(node_type='operator', value=node.op.__class__.__name__,
                    left=convert_ast_node(node.values[0]), right=convert_ast_node(node.values[1]))
    elif isinstance(node, ast.Compare):
        return Node(node_type='operator', value=node.ops[0].__class__.__name__,
                    left=convert_ast_node(node.left), right=convert_ast_node(node.comparators[0]))
    elif isinstance(node, ast.Name):
        return Node(node_type='operand', value=node.id)
    elif isinstance(node, ast.Constant):
        return Node(node_type='operand', value=node.value)
    # Add other node types as needed
    raise ValueError("Unsupported AST Node Type")

def evaluate_rule(ast_node, data):
    """ Recursively evaluate the AST against the data. """
    if ast_node.type == 'operand':
        return data[ast_node.value]
    elif ast_node.type == 'operator':
        left_value = evaluate_rule(ast_node.left, data)
        right_value = evaluate_rule(ast_node.right, data)

        if ast_node.value == 'And':
            return left_value and right_value
        elif ast_node.value == 'Or':
            return left_value or right_value
        elif ast_node.value in ['Gt', 'Lt', 'Eq']:
            if ast_node.value == 'Gt':
                return left_value > right_value
            elif ast_node.value == 'Lt':
                return left_value < right_value
            elif ast_node.value == 'Eq':
                return left_value == right_value
    raise ValueError("Unsupported AST evaluation")

def convert_ast_node(node):
    """ Convert AST node to a JSON serializable dict. """
    if isinstance(node, ast.AST):
        return {
            "type": type(node).__name__,
            "fields": {k: convert_ast_node(v) for k, v in ast.iter_fields(node)}
        }
    else:
        return node
