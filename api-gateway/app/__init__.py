from flask import Flask, jsonify, request
import requests
from requests.exceptions import ConnectionError
import json
import os

app = Flask(__name__)

services = [
    {
        'port': '5001',
        'info_endpoint': 'info',
        'name': 'books',
        'host': os.getenv('BOOKS_HOST')
    },
    {
        'port': '5002',
        'info_endpoint': 'info',
        'name': 'cars',
        'host': os.getenv('CARS_HOST')
    },
]

@app.route('/info')
def info():
    info = {'gateway': True, 'available_services': []}
    for service in services:
        try:
            # response = requests.get(f"http://0.0.0.0:{service['port']}/{service['info_endpoint']}")
            # response = requests.get(f"http://{service['host']}:{service['port']}/{service['info_endpoint']}")
            response = requests.get(f"http://0.0.0.0:{service['port']}/{service['info_endpoint']}")
            r = json.loads(response.text)
            info['available_services'].append(r)
        except ConnectionError:
            pass
    return jsonify(info)

@app.route('/')
def index():
    return jsonify({'ok': True})
