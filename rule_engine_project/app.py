from flask import Flask, request, jsonify
from pymongo import MongoClient
from rule_engine import create_rule, evaluate_rule, convert_ast_node, Node

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Adjust this if using MongoDB Atlas
db = client['rule_engine_db']
rules_collection = db['rules']


@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json.get('rule')
    try:
        # Create the AST using your existing method
        rule_ast = create_rule(rule_string)

        # Convert the AST to a serializable format
        rule_ast_serializable = convert_ast_node(rule_ast)

        # Store rule in MongoDB as a dictionary
        rule_doc = {
            "rule_string": rule_string,
            "rule_ast": rule_ast_serializable  # Store the serializable AST
        }
        rules_collection.insert_one(rule_doc)

        return jsonify({"status": "success", "message": "Rule created"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json.get('data')

    # Retrieve all rules from MongoDB
    stored_rules = list(rules_collection.find({}))

    if not stored_rules:
        return jsonify({"status": "error", "message": "No rules available"}), 400

    # Evaluate the first rule in the collection
    rule_ast_dict = stored_rules[0]['rule_ast']

    # Convert back to Node object
    rule_ast = convert_dict_to_node(rule_ast_dict)

    result = evaluate_rule(rule_ast, data)

    # Optionally return the AST as well
    return jsonify({"status": "success", "result": result, "ast": rule_ast_dict})


def convert_dict_to_node(data):
    """ Convert a dictionary representation of an AST back to Node objects. """
    if data['type'] == 'Constant':
        return Node(node_type='operand', value=data['value'])
    elif data['type'] == 'Name':
        return Node(node_type='operand', value=data['fields']['id'])
    elif data['type'] == 'Compare':
        return Node(node_type='operator', value=data['fields']['ops'][0]['__name__'],
                    left=convert_dict_to_node(data['fields']['left']),
                    right=convert_dict_to_node(data['fields']['comparators'][0]))
    elif data['type'] == 'BoolOp':
        return Node(node_type='operator', value=data['fields']['op']['__name__'],
                    left=convert_dict_to_node(data['fields']['values'][0]),
                    right=convert_dict_to_node(data['fields']['values'][1]))
    # Add other types as necessary based on your AST structure
    raise ValueError("Unsupported AST Node Type")


if __name__ == '__main__':
    app.run(debug=True)
