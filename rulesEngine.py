import Parser as p
import Digestor as dig
import DbDriver as drvr
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from bson.json_util import dumps
import logging
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

print('[+] Iniciando motor de reglas . . .')
parser = p.Parser()	
mongo = drvr.DbDriver('./properties.ini')
digestor = dig.Digestor(mongo)

@app.route('/ruleEngine/create', methods=['POST'])
def createRule():
	data = request.get_data()    
	if parser.parseIn(data):
		mongo.insert(json.loads(data))
		return jsonify(response='ok',code=201)
	return jsonify(response='bad request', code = 403)

@app.route('/ruleEngine/update', methods=['PUT'])
def updateRule():
	data = request.get_data()
	ruleId = request.args.get('id')
	if parser.parseIn(data):
		mongo.update(ruleId, json.loads(data))
		return jsonify(response='ok',code=200)
	return jsonify(response='bad request', code = 403)

@app.route('/ruleEngine/digestor', methods=['POST'])
def digestRule():
	data = request.get_data()
	digestor.digest(data)
	return jsonify(response='ok',code=201)

@app.route('/ruleEngine/rules', methods=['GET'])
def getRules():
	data = mongo.findAll()
	return dumps(data)

@app.route('/ruleEngine/drop', methods=['POST'])
def dropRules():
	mongo.drop()
	return jsonify(response='ok',code=201)

@app.route('/ruleEngine/delete/<id>')
def deleteRule(id):
	return jsonify(response='ok',code=201)

	
if __name__ == "__main__":	
	app.run(debug= True, host= '0.0.0.0')