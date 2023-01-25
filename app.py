from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from db import User, Reservation, Restaurant, Table
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



db.init_app(app)
def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")

###########
#Tablebooking ist die Reservier-Methode

@app.route("/tablebooking")
def tablebooking():
    return render_template("tablebooking.html")

@app.route('/tablebooking', methods=['GET', 'POST'])
def tablebooking():
    if 'email' in session:
        if request.method == 'POST':
            customer_id = User.query.filter_by(email=session['email']).first()
            restaurant_id = request.form['restaurant']
            table_count = request.form['table_count']
            booking_time = request.form['booking_time']
            booking = Booking(customer_id=customer_id, restaurant_id=restaurant_id, table_count=table_count, booking_time=booking_time)
            db.session.add(booking)
            db.session.commit()
            restaurant_email = User.query.filter_by(id=restaurant_id).first().email
            send_email(restaurant_email, 'New Booking Request', 'You have a new booking request.')
            return redirect('/')
        restaurants = User.query.filter_by(user_type='restaurant').all()
        return render_template('tablebooking.html', restaurants=restaurants)
    return redirect('/login')

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
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')     
        password2 = request.form.get('password2')

        if len(email) < 4:
            #mit der flashmessage zeigen wir dem user, was er/sie beim Signup zu beachten hat, flash wurden kategorisiert, um sie farblich anzupassen
            flash('Email must be greater than 3 characters.', category='error')
            pass
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
            pass
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            pass
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            pass
        else:
            #user wird kreiert und zur database hinzugefügt
            #die function "generate_password_hash" encrypted das vom user eingegebene Passwort 
            #"sha256" ist ein Hasing Algorhythmus, der empfolen wird.
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created.', category='success')
            return redirect(url_for('home'))

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