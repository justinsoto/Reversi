from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # fix type of database, database name, and local path

    db.init_app(app)

    from .views import main #importing down here to avoid circular inputs, since the flask app has not been created yet
    app.register_blueprint(main)
    return app

# two API endpoints in views.py. 