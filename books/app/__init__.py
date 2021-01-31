from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/info')
def hello_service():
    return jsonify({'name': 'books'})

@app.route('/')
def index():
    return jsonify({
        'data': [
            {
                'author': 'Carlos Ruiz Zafon',
                'model': 'The Shadow of a Wind'
            },
            {
                'author': 'Lewiss Carroll',
                'model': 'Alice in Wonderland'
            },
        ]
    })