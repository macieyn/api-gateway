from flask import Flask, jsonify, request
import requests
from requests.exceptions import ConnectionError
import json
import os

app = Flask(__name__)

class Service:
    
    def __init__(self, name, host, port, info_endpoint):
        self.name = name
        self.host = host
        self.port = port 
        self.info_endpoint = info_endpoint
        self.request = requests
        self.is_alive = self.ping()

    def info(self):
        response = self.request.get(f"http://{self.host}:{self.port}/{self.info_endpoint}")
        return json.loads(response.text)

    def ping(self):
        try:
            self.request.get(f"http://{self.host}:{self.port}/{self.info_endpoint}")
            return True
        except ConnectionError:
            return False

    def get(self, endpoint):
        response = self.request.get(f"http://{self.host}:{self.port}/{endpoint}")
        return json.loads(response.text)

    def post(self, endpoint, **kwargs):
        response = self.request.post(f"http://{self.host}:{self.port}/{endpoint}", **kwargs)
        return json.loads(response.text)


services = {
    'books': Service(os.getenv('BOOKS_NAME'), os.getenv('BOOKS_HOST'), os.getenv('BOOKS_PORT'), os.getenv('BOOKS_INFO')),
    'cars': Service(os.getenv('CARS_NAME'), os.getenv('CARS_HOST'), os.getenv('CARS_PORT'), os.getenv('CARS_INFO')),
}


@app.route('/info')
def info():
    return jsonify({'name': 'gateway'})


@app.route('/')
def index():
    return jsonify({'ok': True})


@app.route('/services')
def services_info():
    data = { 'services': [] }
    for service in services.values():
        try:
            response = service.info()
            data['services'].append(response)
        except ConnectionError:
            pass
    return jsonify(data)


@app.route('/services/<string:service>/<path:path>', methods=('GET', 'POST'))
def call_service(service, path):
    if request.method == 'GET':
        data = services[service].get(path)
        return jsonify(data)
    elif request.method == 'POST':
        data = services[service].post(path, json=json.dumps(request.json))
        return jsonify(data)
