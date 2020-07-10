from pymongo import MongoClient
from pathlib import Path
from bson.objectid import ObjectId
import configparser

class DbDriver():
    def __init__(self, configPath):
        # Inicio la base
        print('[+] Cargando configuracion . . . ')
        try:                        
            self.config = configparser.ConfigParser()
            self.config.read(Path(configPath))
            self.instanceIp = self.config['dev']['instanceIp']
            self.instancePort = self.config['dev']['instancePort']
            self.collectionName = self.config['dev']['collectionName']
            
            self.client = MongoClient(self.instanceIp, int(self.instancePort))
            self.db = self.client.shaffiro

            print('[+] Configuracion cargada con exito')            
        except ValueError as identifier:
            print('[-] Error al cargar configuracion')

    # Busca en la base y devuelve un cursor con las reglas halladas.
    def find(self, data):
        try:
            return self.db.reglas.find(data)
        except ValueError:
            print('[-] Error')

    # Inserta en la base
    def insert(self, data):
        try:
            print('[+] Insertando regla . . . ')
            return self.db.reglas.insert_one(data)
        except ValueError as identifier:
            print('[-] Error')
    def findAll(self):
        try:
            return self.db.reglas.find()
        except ValueError as identifier:
            print('[-] Error')

    # Actualiza una regla
    def update(self, ruleId, data):
        try:
            print('[+] Actualizando regla . . . ')
            return self.db.reglas.replace_one({ "_id": ObjectId(ruleId) }, data)
        except ValueError as identifier:
            print('[-] Error')
