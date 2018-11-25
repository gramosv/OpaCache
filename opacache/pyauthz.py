from flask import Flask, jsonify, request
import requests
import hashlib
import json
import sys
import os
import io
import logging
import redis
import ast
import configparser

# START APP
app = Flask(__name__)

# CONFIGURATION FILE
config = configparser.ConfigParser()
config.read('/data/config.ini')

# CONFIGURATION PROPERTIES
opa_host = config['DEFAULT']['OPA_HOST']
cache_port = config['DEFAULT']['CACHE_PORT']
debug_enabled = config['DEFAULT']['DEBUG_ENABLED']
ttl = config['DEFAULT']['TTL_SECONDS']

# REDIS CONNECTION PROPERTIES
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# LOGGING PROPERTIES

if (debug_enabled == "false"):
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.ERROR)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:uri>', methods=['POST'])
def authz(uri):
	# Obtener peticion de autorizacion
	payload = request.json
	# Hashear peticion de autorizacion
	m = hashlib.md5()
	m.update((json.dumps(payload) + uri).encode("utf-8"))
	hashedData = m.hexdigest()	
	# Comprobar si la cache ya tiene el hash
	if redisGet(hashedData):
		# La peticion esta cacheada: devolvemos el valor cacheado
		return jsonify(ast.literal_eval(redisGet(hashedData))), 200
	else:
		# La peticion no esta cacheada: Preguntamos a OPA
		resp = requests.post(opa_host + "/" + uri, data=json.dumps(payload), verify = False)
		authzResponse = json.loads(resp.text)
		# Cacheamos respuesta
		redisSet(hashedData, authzResponse)
		# Devolvemos el valor 		
		return jsonify(authzResponse), 200

def redisGet(key):
	return r.get(key)

def redisSet(key, value):
	r.set(key, value, ex=ttl)

# START SERVER
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=cache_port)


