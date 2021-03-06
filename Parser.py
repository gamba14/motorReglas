import json
class Parser():

	def parseIn(self, inJson):
		try:
			rule = json.loads(inJson)
			#sabemos que las posiciones 0:id, 1:nombre,2:list<Antecedentes>,3:list<consecuentes>
			#sabemos tambien que los antecedentes y consecuentes tienen estructura. validemos la estructura
			antecedents = self.validateConsistency(rule['antecedents'])
			consequences = self.validateConsistency(rule['consequences'])
			#hay que verificar que la regla tenga sentido
			if (antecedents and consequences):
				print("[+] Regla: valida")
				return True
			print("[-] Regla: no valida")
			return False
		except ValueError:
			print("[-] Error al parsear JSON")
			return False

	#Evalua si antecedentes y consecuentes estan balanceados
	def validateConsistency(self, inData):
		termSize = len(inData)
		if termSize == 0:
			return False
		con = 0
		cond = 0
		for term in inData:
			if 'conector' in term:
				con += 1
			else:
				cond += 1	
		return cond == con + 1

	# def main():
	# 	print("Reading form file")
	# 	with open('/home/agustin/proyectos/pyRuleEngine/rule.txt','r') as f:
	# 		data = f.read()		
	# 	if parseIn(data):
	# 		#Salvo la regla
	# 		print("Persisto")
	# 		mongo.insert(data)
	# 	else:
	# 		print("No persisto")

	# if __name__ == "__main__":
	# 	main()


