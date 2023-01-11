from . import db
from flask import Flask 
from datetime import datetime
from flask_login import UserMixin

#database models
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True) #id wird automatisch bei database-eintrag erstellt
    reservationname = db.Column(db.String(50), nullable=False) #nullable besagt, dass das Feld ausgefüllt werden muss
    reservationemail = db.Column(db.String(120), nullable=False, unique=True) #unique, damit es jede Email nur einmal geben wird
    reservationdate_added = db.Column(db.DateTime, default=datetime.utcnow) #Return the current UTC date and time, with tzinfo None. --> https://docs.python.org/3/library/datetime.html
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("table.id"), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #id wird automatisch bei database-eintrag erstellt
    name = db.Column(db.String(50), nullable=False) #nullable besagt, dass das Feld ausgefüllt werden muss
    email = db.Column(db.String(120), nullable=False, unique=True) #unique, damit es jede Email nur einmal geben wird
    password_hash = db.Column(db.String(100))
    role = db.Column(db.String(20)) #entscheidet, ob es ein restaurant ist oder restaurantbesucher
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #Return the current UTC date and time, with tzinfo None. --> https://docs.python.org/3/library/datetime.html
    reservations = db.relationship("Reservation", backref="user", lazy=True)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    tables = db.relationship("Table", backref="restaurant", lazy=True)
    
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    reservations = db.relationship("Reservation", backref="table", lazy=True)

#blog data model muss hier noch hin
        



