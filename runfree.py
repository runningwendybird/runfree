# This is the controller file. All of my routes for my flask app
# will go here. 

from flask import Flask, request, render_template, g, redirect, url_for, flash
from flask import session as flask_session
import model
import jinja2
import os
from datetime import datetime, date


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

@app.route("/authenticate", methods=["POST"])
def authenticate_user():
	"""checks to see if the user is in the database and checks password"""

	# gets email and password
	email = request.form.get("email")
	password = request.form.get("password")
	user = model.get_user_by_email(email)

	# if email not in the database, redirects to a sign up page.
	if user == None:
		flash("Please sign up!")
		
		return redirect("/new_user")
	
	# if password does not match what is in the database, asks user to try again.  
	if user.password != password:
		flash("The password you entered is incorrect. Please try again.")

		return redirect("/")
	
	# adds email to session. Redirects to run_log. 
	flask_session["email"] = model.get_user_by_email(email).email
	flash("Successfully logged in!")

	return redirect("/run_log")

@app.route("/new_user")
def add_user():
	"""Sends the user to the sign up form."""
	return render_template("new_user.html")

@app.route("/add_user", methods=["POST"])
def insert_user():
	"""Adds user to the database."""

	# Pulling out all the info from the sign up form. 

	email = request.form.get("email")
	password = request.form.get("password")
	passwordcheck = request.form.get("passwordcheck")
	first = request.form.get("first_name")
	last = request.form.get("last_name")
	birthdate = request.form.get("birthdate")
	# Converting the birthdate to a datetime object.
	birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
	sex = request.form.get("sex")
	zipcode = request.form.get("zipcode")

	# Checking to be sure that the user entered the password as desired.
	# Will redirect them back to the form if not. 
	if password != passwordcheck:
		flash("Your passwords do not match. Please refill out the form.")
		return redirect("/new_user")

	# Checking to be sure that the new user filled out the form in its entirety.
	# Will redirect them back to the form if not. 

	user_info = [email, password, first, last, birthdate, sex, zipcode]
	print user_info

	if None in user_info:
		flash("You must fully fill out the form. Please try again.")
		return redirect("/new_user")

	# Creating a user object with the user's information. 
	new_user = model.User(email=email, password=password, first=first, last=last, birthdate=birthdate, sex=sex, zipcode=zipcode )
	
	# Adding the user to the database. 
	model.insert_new_user(new_user)

	# storing their email in the session. 
	flask_session["email"] = email

	return redirect("/run_log")

# These Routes are for navigating the functionality 
# of the app once you are logged in. 

@app.route("/run_log")
def display_log():
	"""Displays links to review the previous runs."""

	if flask_session.get("email") == None:
		flash("You must sign in to view that page.")
		
		return redirect("/")
	
	else:
		user = model.get_user_by_email(flask_session["email"])

		runs = model.find_all_runs(user)


		return render_template("run_log.html", user = user, runs = runs)

@app.route("/new_run")
def new_run():
	"""Renders the form the user completes to add a run."""
	return render_template("new_run.html")

@app.route("/add_run", methods = ["POST"])
def add_run():
	# User Object
	user = model.get_user_by_email(flask_session["email"])
	
	# Getting info from the form. 
	date_run = request.form.get("new_run_date_and_time")
	print date_run
	date_run = datetime.strptime(date_run, "%Y-%m-%dT%H:%M")
	zipcode = request.form.get("zipcode")
	distance = float(request.form.get("distance"))
	duration = int(request.form.get("duration"))
	pre_run = int(request.form.get("pre_run"))
	during_run = int(request.form.get("during_run"))
	post_run = int(request.form.get("post_run"))
	energy = int(request.form.get("energy"))
	feeling = request.form.get("feeling")
	location = request.form.get("location")
	terrain = request.form.get("terrain")
	route = request.form.get("route")
	thoughts = request.form.get("thoughts")

	# Creating a new run and adding it to the database.

	new_run = model.Run(user_id = user.id, date_run = date_run, zipcode=zipcode, approx_dist = distance, approx_time = duration)
	model.insert_new_run(new_run)
	new_run_object = model.get_run_by_datetime(date_run)

	# Creating rating objects. 

	pre_run = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 1, numeric_ans = pre_run)
	during_run = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 2, numeric_ans = during_run)
	post_run = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 3, numeric_ans = post_run)
	energy = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 4, numeric_ans = energy)
	
	feeling = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 5, select_ans = feeling)
	location = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 6, select_ans = location)
	terrain = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 7, select_ans = terrain)
	route = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 8, select_ans = route)
	
	thoughts = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 9, text_ans = thoughts)
	
	# Adding rating objects to database.
	ratings = [pre_run, during_run, post_run, energy, feeling, location, terrain, route, thoughts]
	for rating in ratings:
		model.sqla_session.add(rating)

	model.sqla_session.commit()

	return redirect("/run_log")

@app.route("/view_run.html")
def review_run():
	current_run_id = request.args.get("run_id")
	current_run = model.get_run_by_id(current_run_id)
	return render_template("view_run.html", run=current_run)


@app.route("/run_graphs")
def display_progress():
	
	return render_template("data_vis.html")


@app.route("/goals")
def set_goals():

	user = model.get_user_by_email(flask_session["email"])

	goals = user.goals

	return render_template("goal_log.html" , goals = goals)

@app.route("/new_goal")
def new_goal():
	"""Renders the form the user completes to add a goal."""
	return render_template("new_goal.html")

@app.route("/add_goal", methods=["POST"])
def add_goal():
	"""Adds a goal to the database when the user submits the new goal form."""
	user = model.get_user_by_email(flask_session["email"])
	goal = request.form.get("goal")
	fitness_level = request.form.get("fitness_level")
	run_length_history = request.form.get("run_length_history")
	set_date = date.today()


	new_goal = model.Goal(user_id = user.id, description=goal, fitness_level=fitness_level, run_length_history=run_length_history, set_date=set_date)

	model.insert_new_goal(new_goal)

	return redirect("/goals")

# These Routes are for logging you out. 

@app.route("/sign_out")
def end_session():

	flask_session.pop("email", None)

	return redirect("/")







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)