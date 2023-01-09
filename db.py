from . import db
from flask import Flask 
from datetime import datetime
from flask_login import Usermixin

#database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) #id wird automatisch bei database-eintrag erstellt
    name = db.Column(db.String(50), nullable=False) #nullable besagt, dass das Feld ausgefüllt werden muss
    email = db.Column(db.String(120), nullable=False, unique=True) #unique, damit es jede Email nur einmal geben wird
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #Return the current UTC date and time, with tzinfo None. --> https://docs.python.org/3/library/datetime.html

