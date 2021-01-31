from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/info')
def hello_service():
    return jsonify({'name': 'cars'})

@app.route('/')
def index():
    return jsonify({
        'data': [
            {
                'manufacturer': 'Ford',
                'model': 'Mustang'
            },
            {
                'manufacturer': 'Chevrolet',
                'model': 'Camaro'
            },
        ]
    })