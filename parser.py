import json

def parseIn(inJson):
	try:
		rule = json.loads(inJson)
		#sabemos que las posiciones 0:id, 1:nombre,2:list<Antecedentes>,3:list<consecuentes>
		#sabemos tambien que los antecedentes y consecuentes tienen estructura. validemos la estructura
		antecedents = validateConsistency(rule['antecedents'])
		consequences = validateConsistency(rule['consequences'])
		#hay que verificar que la regla tenga sentido
		if (antecedents and consequences):
			print("es valida")
			return True
		print("no es valida")
		return False
	except ValueError:
		print("Error al parsear JSON")
		return False

#Evalúa si antecedentes y consecuentes estan balanceados
def validateConsistency(inData):
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

def main():
	print("Reading form file")
	with open('/home/agustin/proyectos/pyRuleEngine/rule.txt','r') as f:
		data = f.read()		
	if parseIn(data):
		#Salvo la regla
		print("Persisto")
	else:
		print("No persisto")

if __name__ == "__main__":
	main()


