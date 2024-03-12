# app.py (Flask App to serve as backend)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def main_page():
    return "Main Page"

@app.route('/hello')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
