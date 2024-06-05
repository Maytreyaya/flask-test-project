from flask import jsonify
from flask import request
from jsonrpcserver import method, Success, dispatch

@method
def add(a, b):
    return Success(a + b)


@app.route('/jsonrpc', methods=['POST'])
def jsonrpc():
    response = dispatch(request.data)
    return jsonify(response)