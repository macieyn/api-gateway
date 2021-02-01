from flask import Flask, jsonify ,request
import json


app = Flask(__name__)


collection = [
    {
        'author': 'Carlos Ruiz Zafon',
        'model': 'The Shadow of a Wind'
    },
    {
        'author': 'Lewiss Carroll',
        'model': 'Alice in Wonderland'
    },
]


@app.route('/info')
def hello_service():
    return jsonify({'name': 'cars'})


@app.route('/api', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return jsonify({
            'data': collection 
        })
    elif request.method == 'POST':
        app.logger.info('Incomming POST request')
        new_item = json.loads(request.json)
        collection.append(new_item)
        app.logger.info(f'New car was added')
        return jsonify(new_item)