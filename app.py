from website import create_app
from website import db
from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from website.db import User, Reservation, Restaurant, Table
from werkzeug.security import check_password_hash, generate_password_hash
import smtplib

#kreiert Flask Instance
app = Flask(__name__)
app.secret_key = 'key123'
#fügt eine database hinzu (https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initiiert die database
db = SQLAlchemy(app)
DB_Name = "database.db"






@app.route("/")
def home():
    return render_template('index.html')

###########
#Tablebooking ist die Reservier-Methode

@app.route("/tablebooking", methods=['GET', 'POST'])
def tablebooking():
    #Überprüft, ob ein Benutzer eingeloggt ist
    if 'email' in session:
        #Wenn der Request-Method POST ist, wird die Reservierung erstellt
        if request.method == 'POST':
            #Der aktuelle Benutzer usw., werden aus der Datenbank abgerufen

            customer = User.query.filter_by(email=session['email']).first()
            restaurant = Restaurant.query.filter_by(id=request.form['restaurant']).first()
            table = Table.query.filter_by(id=request.form['table']).first()
            reservation_time = request.form['reservation_time']
        #Eine neue Reservierung wird erstellt
            reservation = Reservation(user=customer, table=table, reservation_time=reservation_time)
        #Neue Reservierung wird in die Datenbank hinzugefügt
            db.session.add(reservation)
            db.session.commit()
        #Email-Adresse des Restaurants wird abgerufen
            restaurant_email = User.query.filter_by(id=restaurant.id).first().email
        #Die Email wird an das Restaurant gesendet
            send_email(restaurant_email, 'New Reservation Request', 'You have a new reservation request.')
        #Die Email, mit der sich der User gerade in der Session befindet 
            send_email(session['email'], 'Your Reservation', 'Your reservation request has been received and is being processed. The restaurant ower will contact you and confirm your reservation. thanks TB') 
            flash("Reservation request submitted successfully", category='success')
            return redirect('/')
        restaurants = Restaurant.query.all()
        return render_template('tablebooking.html', restaurants=restaurants)
    

def send_email(to, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    msg = f"Subject: {subject}\n\n{message}"
    server.sendmail('your_email@gmail.com', to, msg)
    server.quit()

##########

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        #Überprüfung, ob die E-Mail bereits registriert ist
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email is already registered", category='danger')
            return redirect("/signup")
        
        #Überprüfung, ob das Passwort gültig ist 
        if len(password) < 8:
            flash("Password must be at least 8 characters", category='danger')
            return redirect("/signup")

        #Hash das Passwort
        password_hash = generate_password_hash(password)

        # Erstellen und Speichern des neuen Benutzers in der Datenbank
        new_user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful, please login", category='success')
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST": 
        username = request.form["email"]
        password = request.form["password"]
        session["user"] = username
        #mit der flashmessage zeigen wir dem user, dass er sich eingeloggt hat
        flash("Login successful")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            #mit der flashmessage zeigen wir dem user, dass er bereits eingeloggt ist
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user(): 
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        #mit der flashmessage zeigen wir dem user, dass er sich erst einloggen muss und falsch auf der Seite ist 
        flash("You're not logged in.", category="error")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
     #mit der flashmessage zeigen wir dem user, dass er sich ausgeloggt hat
    flash(f"You logged out successfully", "info")
    #mit session.pop löschen wir die Daten aus der session beim Ausloggen, beim wieder einloggen ist es auch nicht mehr zu sehen
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)