from lexic import lexic_analyzer, Token_enum, Token_dict, InvalidTokenException

import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin

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
    except InvalidTokenException as e:
        return jsonify({"error": str(e)}), 200
    
    # return json

    # output code 
    processed_text = ''
    for match in new_matches:
        processed_text += match.match + ' '

    return jsonify({
        "output": processed_text,
        "tokens": [{
        "token": match.token.comentary,
        "value": match.match,
        "line": match.line,
        "span": f'{match.span[0]}, {match.span[1]}'
    } for match in new_matches]}), 200

if __name__ == '__main__':
    app.run(debug=True)