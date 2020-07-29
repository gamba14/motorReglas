import DbDriver as dbd
import json
import functools
import datetime
import requests
from dateutil.parser import *

class Digestor():

	def __init__(self, driver):
		print('[+] Inicializando digestor . . .')
		self.mongo = driver
		
	# El digestor tiene que recibir la entrada y no tiene que devolver nada al cliente
	# Tiene que analizar las entradas y tomar la decision manda {"id",{0,1}} depende el valor.
	def digest(self, data):
		results = []
		print('[+] Recibo: ', end='\t')
		print(data)
		dataJson = json.loads(data)
		idDisp = "{\"antecedents.id1\":" + str(dataJson['id']) + "}"
		# El cursor va a tener todas las reglas que matcheen con el id del dispositivo	
		cursor = self.mongo.find(json.loads(idDisp))
		self.curTime = datetime.datetime.today()	
		for regla in cursor:
			print(regla)
			results.append(self.ruleEval(regla['antecedents'],dataJson["pv"]))
		for result in results:
			# strJson = "{\"id\":" + str(dataJson['id']) +"\",\"action\":\"" + str(result) + "\"}"
			strJson = {'action' : str(result), 'id' : str(dataJson['id'])}
			# self.sendToBroker(json.dumps(strJson))
			self.sendToBroker(strJson)


	# Funcion que devuelve al broker la accion a tomar
	def sendToBroker(self,data):
		newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		url = 'http://docker_shaffiro-app_1:8080/api/receiveAction'
		requests.post(url, data, headers = newHeaders)

	def ruleEval(self,antecedents, pv):
		results = [] #0 si no se cumple 1 si se cumple, -1 si no hace nada
		conectors = [] #0 es una OR y 1 es una and
		for antecedent in antecedents:
			if not 'conector' in antecedent:
				operator = antecedent['op']
				vs = antecedent['vs']
				unit = antecedent['unit']
				if unit != "horas":
					if operator == '>':
						results.append(1 if int(pv) > int(vs) else 0)
					elif operator == '<':
						results.append(1 if int(pv) < int(vs) else 0) #100 749
					else:
						if(int(vs) == pv):
							results.append(-1)
				else:					
					if operator == '>':
						results.append(1 if parse(vs) < self.curTime else 0)
					elif operator == '<':
						results.append(1 if parse(vs) > self.curTime else 0)
					else:
						results.append(-1)

			else:
				if '&&' in antecedent:
					conectors.append(1)
				else:
					conectors.append(0)
		print(results)
		print(conectors)
		# Armar la compuerta dinamica
		# Caso trivial, cuando hay una sola condicion.
		if len(conectors) == 0:
			return results[0]		
		if sum(conectors) == 0:
			if sum(results) > 0 : return 1
			return 0
		else:
			return functools.reduce(lambda x,y: x*y, results)		

	# def main():
	# 	print("Reading form file")
	# 	with open('/home/agustin/proyectos/pyRuleEngine/message.txt','r') as f:
	# 		data = f.read()	
	# 		digest(data)
	# if __name__ == "__main__":
	# 	main()