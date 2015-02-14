# This is the controller file. All of my routes for my flask app
# will go here. 

from flask import Flask, request, render_template, g, redirect, url_for, flash
from flask import session as flask_session
import model
import jinja2
import os

# App information

app = Flask(__name__)
app.secret_key = "THISISMYPRODUCTIONANDTESTINGKEY"
app.jinja_env.undefined = jinja2.StrictUndefined

# Routes Begin Here

# These Routes are for navigating before you log in. 

@app.route("/")
def landing_page():
	return render_template("landing.html")

@app.route("/about")
def about_runfree():
	return render_template("about_runfree.html")

@app.route("/business")
def display_business_info():
	return render_template("business_card.html")


# These Routes are for logging in. 

# These Routes are for navigating the functionality 
# of the app once you are logged in. 

@app.route("/authenticate", methods=["POST"])
def authenticate_user():
	email = request.form.get("email")
	password = request.form.get("password")

	if model.get_user_by_email == None:
		flash("Please sign up!")
		
		return redirect("/new_user")
	
	else:
		flask_session["email"] = model.get_user_by_email(email).email
		flash("Successfully logged in!")

	return redirect("/run_log")

@app.route("/new_user")
def add_user():
	return render_template("new_user.html")

@app.route("/add_user", methods=["POST"])
def add_user():
	email = request.form.get("email")
	password = request.form.get("password")


	new_user = model.User(email=email, password=password)
	model.insert_new_user(new_user)

	flask_session["email"] = email

	return rredirect("/run_log")

# These Routes are for logging you out. 

@app.route("/run_log")
def display_log():
	if flask_session.get("email") == None:
		flash("You must sign in to view that page.")
		
		return redirect("/")
	
	else:
		user = model.get_user_by_email(flask_session["email"])

		return render_template("run_log.html")












if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)