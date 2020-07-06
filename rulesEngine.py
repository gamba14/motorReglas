import Parser as p
import Digestor as dig
import DbDriver as drvr
import json
from flask import Flask, request, jsonify
from bson.json_util import dumps
app = Flask(__name__)

print('[+] Iniciando motor de reglas . . .')
parser = p.Parser()	
mongo = drvr.DbDriver('/home/agustin/proyectos/pyRuleEngine/properties.ini')
digestor = dig.Digestor(mongo)

@app.route('/ruleEngine/create', methods=['POST'])
def createRule():
	data = request.get_data()    
	if parser.parseIn(data):
		mongo.insert(json.loads(data))
		return jsonify(response='ok',code=201)
	return jsonify(response='bad request', code = 403)

@app.route('/ruleEngine/digestor', methods=['POST'])
def digestRule():
	data = request.get_data()
	digestor.digest(data)
	return jsonify(response='ok',code=201)

@app.route('/ruleEngine/rules', methods=['GET'])
def getRoutes():
	data = mongo.findAll()
	return dumps(data)

if __name__ == "__main__":	
	app.run()