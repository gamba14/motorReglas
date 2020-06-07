import parser as p
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/ruleEngine/create', methods=['POST'])
def createRule():
    data = request.get_data()    
    if p.parseIn(data):
        return jsonify(response='ok',code=201)
    return jsonify(response='bad request', code = 403)