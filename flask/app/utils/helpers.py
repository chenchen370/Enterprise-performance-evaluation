from flask import jsonify

def format_response(data, status_code=200):
    return jsonify(data), status_code