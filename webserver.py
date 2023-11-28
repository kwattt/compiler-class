from lexic import *

import flask
from flask import request, jsonify
from flask_cors import CORS

from syntax import parse_program, program_to_tree, ParserUnexpectedEnd, ParserUnexpectedType
from semantic import SemanticAnalyzer, SemanticError

app = flask.Flask(__name__)
cors = CORS(app , resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Lexico-api</h1>'''

@app.route('/api/v1/lexico', methods=['POST'])
def v1_lexico():
    # json data from request
    data = request.get_json()

    # get code from json
    code = data['code']
    # parse code
    try:
        new_matches = lexic_analyzer(code)
    except LexicInvalidToken as e:
        return jsonify({"error": str(f"LexicError: {e}")}), 200
    
    # return json

    # output code 
    processed_text = ''
    for match in new_matches:
        processed_text += match.match + ' '
    try:
        parsed_code = parse_program(new_matches)
    except ParserUnexpectedEnd as e:
        return jsonify({"error": str(f"SyntaxError: {e}")}), 200
    except ParserUnexpectedType as e:
        return jsonify({"error": str(f"SyntaxError: {e}")}), 200

    #try:
    #    sem = SemanticAnalyzer(parsed_code)
    #    sem.analyze()
    #except SemanticError as e:
    #    return jsonify({"error": str(f"SemanticError: {e}")}), 200

    tree_dict = program_to_tree(parsed_code)

    return jsonify({
        "output": processed_text,
        "tokens": [{
            "token": match.token.comentary,
            "value": match.match,
            "line": match.line,
            "span": f'{match.span[0]}, {match.span[1]}',
        } for match in new_matches],
        "tree": tree_dict
    }), 200

if __name__ == '__main__':
    app.run(debug=True)