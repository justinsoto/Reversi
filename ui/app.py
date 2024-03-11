# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

@app.route('/hello')
def hello():
    return 'Hello, World!'
'''def get_data():
    return jsonify({'message': 'Hello from Flask!'})
'''
if __name__ == '__main__':
    app.run()
