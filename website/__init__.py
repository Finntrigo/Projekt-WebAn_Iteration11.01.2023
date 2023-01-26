from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(app.instance_path, 'database.db')
    db.init_app(app)
    def __init__(self, name, email):
        self.name = name
        self.email = email
    return app
