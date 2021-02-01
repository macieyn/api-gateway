from flask import Flask, jsonify, request
from requests.exceptions import ConnectionError
import requests
import json
import os
from .service import Service 


app = Flask(__name__)


services = {
    'books': Service(os.getenv('BOOKS_NAME'), os.getenv('BOOKS_HOST'), os.getenv('BOOKS_PORT'), os.getenv('BOOKS_INFO')),
    'cars': Service(os.getenv('CARS_NAME'), os.getenv('CARS_HOST'), os.getenv('CARS_PORT'), os.getenv('CARS_INFO')),
    'fake': Service('fake', 'fake', '5000', 'fake'),
}


@app.route('/')
def index():
    return jsonify({'ok': True})


@app.route('/info')
def info():
    return jsonify({'name': 'gateway'})


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
