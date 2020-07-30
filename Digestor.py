import DbDriver as dbd
import json
import functools
import datetime
import requests
import logging
from dateutil.parser import *

class Digestor():

	def __init__(self, driver):
		print('[+] Inicializando digestor . . .')
		self.mongo = driver
		
	# El digestor tiene que recibir la entrada y no tiene que devolver nada al cliente
	# Tiene que analizar las entradas y tomar la decision manda {"id",{0,1}} depende el valor.
	def digest(self, data):
		results = []
		logging.debug(data)
		dataJson = json.loads(data)
		idDisp = "{\"antecedents.id1\":" + str(dataJson['id']) + "}"
		# El cursor va a tener todas las reglas que matcheen con el id del dispositivo	
		cursor = self.mongo.find(json.loads(idDisp))
		self.curTime = datetime.datetime.today()	
		for regla in cursor:
			print(regla)
			id2 = regla['consequences'][0]['id2']
			accion = regla['consequences'][0]['action']
			results.append(self.ruleEval(regla['antecedents'],dataJson["pv"], accion)) #[0,1]		
		if (0 in results):
			strJson = {'action' : '0', 'id' : str(id2)}		
			self.sendToBroker(strJson)
		elif (1 in results):
			strJson = {'action' : '1', 'id' : str(id2)}
			self.sendToBroker(strJson)


	# Funcion que devuelve al broker la accion a tomar
	def sendToBroker(self,data):
		# newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		url = 'http://docker_shaffiro-app_1:8080/api/receiveAction'
		requests.post(url,json= data)

	def ruleEval(self,antecedents, pv, accion):
		valorAccion = 1 if accion == 'on' else 0
		results = [] #0 si no se cumple 1 si se cumple, -1 si no hace nada
		conectors = [] #0 es una OR y 1 es una and
		for antecedent in antecedents:
			logging.debug(antecedent)
			if not 'conector' in antecedent:
				operator = antecedent['op']
				vs = antecedent['vs']
				unit = antecedent['unit']
				if unit != "horas":
					logging.debug('[+] La unidad no es horas')
					if operator == '>':
						logging.debug('[+] Operador >')
						results.append(1 if int(pv) > int(vs) else 0)
					elif operator == '<':
						logging.debug('[+] Operador <')
						results.append(1 if int(pv) < int(vs) else 0) #100 749
					else:
						if(int(vs) == pv):
							results.append(-1)
				else:					
					if operator == '>':
						logging.debug('[+] Operador > en horas')
						results.append(1 if parse(vs) < self.curTime else 0)
					elif operator == '<':
						logging.debug('[+] Operador < en horas')
						results.append(1 if parse(vs) > self.curTime else 0)
					else:
						results.append(-1)

			else:
				if '&&' in antecedent:
					logging.debug('[+] conector &&')
					conectors.append(1)
				else:
					logging.debug('[+] conector ||')
					conectors.append(0)
		logging.debug(results)
		logging.debug(conectors)
		return self.inferrAction(valorAccion,results, conectors)		
	
	def inferrAction(self, accion, results, conectors):
		if len(conectors) == 0:
			if results[0] == 1:
				logging.debug('[+] Sin conectores, regla cumplida >')
				return accion
			else:
				logging.debug('[+] Sin conectores, regla no cumplida >')
				return -1
		if sum(conectors) == 0:
			if sum(results) > 0 :
				logging.debug('[+] Con conectores OR, regla cumplida >') 
				return accion
			logging.debug('[+] Con conectores OR, regla no cumplida >') 	
			return -1
		else:
			if (functools.reduce(lambda x,y: x*y, results) == 1):
				logging.debug('[+] Con conectores AND, regla cumplida >') 
				return accion
			else:
				logging.debug('[+] Con conectores AND, regla no cumplida >') 
				return -1
	