
#from flask import Flask 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from os import path
from werkzeug.security import check_password_hash, generate_password_hash
import click
from app import app

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy()
db.init_app(app)

#database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #id wird automatisch bei database-eintrag erstellt
    name = db.Column(db.String(50), nullable=False) #nullable besagt, dass das Feld ausgefüllt werden muss
    email = db.Column(db.String(120), nullable=False, unique=True) #unique, damit es jede Email nur einmal geben wird
    password_hash = db.Column(db.String(100)) #verändert, das vom User eingegebene Passwort 
    role = db.Column(db.String(20)) #entscheidet, ob es ein restaurant ist oder restaurantbesucher
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #Return the current UTC date and time, with tzinfo None. --> https://docs.python.org/3/library/datetime.html
    reservations = db.relationship("Reservation", backref="user", lazy=True)

    #wenn der User sich einloggt wird überprüft, ob das Passwort valid ist 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True) #id wird automatisch bei database-eintrag erstellt
    reservationname = db.Column(db.String(50), nullable=False) #nullable besagt, dass das Feld ausgefüllt werden muss
    reservationemail = db.Column(db.String(120), nullable=False, unique=True) #unique, damit es jede Email nur einmal geben wird
    reservationdate_added = db.Column(db.DateTime, default=datetime.utcnow) #Return the current UTC date and time, with tzinfo None. --> https://docs.python.org/3/library/datetime.html
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("table.id"), nullable=False)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    tables = db.relationship("Table", backref="restaurant", lazy=True)
    
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    peoplecount = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    reservations = db.relationship("Reservation", backref="table", lazy=True)

#blog data model muss hier noch hin
        

with app.app_context():
	db.create_all()

# run with "flask db-init" from shell
@click.command('db-init')
def init():
	with app.app_context():
		db.drop_all()
		db.create_all()
	click.echo('Database has been initialized.')

app.cli.add_command(init)