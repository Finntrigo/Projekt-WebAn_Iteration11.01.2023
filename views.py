from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

#routes werden in diesem file aufgesetzt, damit die Initiation der main (app.py) sich nciht aufhängt o.Ä.
views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/tablebooking")
def tablebooking():
    return render_template("tablebooking.html")

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
        session["user"] = username
        #mit der flashmessage zeigen wir dem user, dass er sich eingeloggt hat
        flash("Login successful")
        return redirect(url_for("views.user"))
    else:
        if "user" in session:
            #mit der flashmessage zeigen wir dem user, dass er bereits eingeloggt ist
            flash("Already logged in")
            return redirect(url_for("views.user"))
        return render_template("login.html")

@views.route("/user", methode=["POST", "GET"])
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
        flash("You're not logged in.")
        return redirect(url_for("views.login"))

@views.route("/logout")
def logout():
     #mit der flashmessage zeigen wir dem user, dass er sich ausgeloggt hat
    flash(f"You logged out successfully", "info")
    #mit session.pop löschen wir die Daten aus der session beim Ausloggen, beim wieder einloggen ist es auch nicht mehr zu sehen
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("views.login"))