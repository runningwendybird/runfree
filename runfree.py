# This is the controller file. All of my routes for my flask app
# will go here. 

from flask import Flask, request, render_template, g, redirect, url_for, flash, jsonify
from flask import session as flask_session
import model
import jinja2
import os
from datetime import datetime, date, timedelta
import goals
import requests
import json
from math import ceil



# App information

app = Flask(__name__)
app.secret_key = "THISISMYPRODUCTIONANDTESTINGKEY"
app.jinja_env.undefined = jinja2.StrictUndefined

# API keys

ACTIVEDOTCOM_KEY= os.environ["ACTIVEDOTCOM_KEY"]


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

	# I should probably either remove this, or write a general function and 
	# call it for each page behind where the user needs to be logged in. 


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
	"""Allows the user to view a previous run."""
	current_run_id = request.args.get("run_id")
	current_run = model.get_run_by_id(current_run_id)
	current_ratings = model.get_ratings_for_run(current_run_id)
	colors = {}
	for i in range(4):
		if current_ratings[i].numeric_ans < 2:
			colors[i] = "red"
		elif current_ratings[i].numeric_ans < 4:
			colors[i] = "yellow"
		else:
			colors[i] = "green"

	color_zero = colors[0]
	color_one = colors[1]
	color_two = colors[2]
	color_three = colors[3]

	print current_ratings[0], color_zero

	score = model.get_run_score(current_run_id)


	return render_template("view_run.html", run=current_run, ratings = current_ratings, terrain_dictionary = model.terrain_dictionary, route_dictionary = model.route_dictionary, score = score, color_zero = color_zero, color_one = color_one, color_two = color_two, color_three = color_three)



@app.route("/bar_chart")
def bar_chart():
	"""Will send the relevant information to the run graph 
	page in order to construct a bar chart that will show the
	users last five runs."""

	number_of_runs = request.args.get("number_of_runs")

	if number_of_runs == None:
		number_of_runs = 5

	user = model.get_user_by_email(flask_session["email"])

	runs = model.get_collection_of_runs(user.id, runs_to_get = number_of_runs)

	run_list_of_dictionaries = []

	#Changing date in order to jsonify
	for run in runs:
		 run_list_of_dictionaries.append({'date': run[0].strftime("%m-%d-%Y"), 'distance': run[1], "score": run[2]})
	
	print run_list_of_dictionaries

	

	json_runs = json.dumps(run_list_of_dictionaries)
	
	print json_runs

	print type(json_runs)

	return json_runs

@app.route("/pie_chart")
def pie_chart():
	""" Will return the data required to the run graph page
	to create a chart that will show the user the percentage of 
	their runs occur in different locales. """

	user = model.get_user_by_email(flask_session["email"])

	number_of_runs = request.args.get("number_of_runs")

	if number_of_runs == None:
		number_of_runs = 5
	
	location_ratings = model.get_location_ratings(user, runs_to_get = number_of_runs)

	location_dictionary = {}

	colors = ["#1f77b4", "#ff7f0e", "#9467bd", "#17becf", "#bcbd22", "#e377c2", "#8c564b"]
	
	for rating in location_ratings:
		if location_dictionary.get(rating.select_ans) == None:
			location_dictionary[rating.select_ans] = 1
		else:
			location_dictionary[rating.select_ans] = location_dictionary[rating.select_ans] + 1

	location_list = []

	for each_key in location_dictionary.keys():
		location_list.append({"location": each_key.upper(), "occurances": location_dictionary[each_key], "color": colors.pop() })

	

	json_locations = json.dumps(location_list)
	print json_locations
	return json_locations

@app.route("/run_graphs")
def display_progress():

	"""Renders the graph page"""



	return render_template("data_vis.html")


@app.route("/goals")
def set_goals():
	"""Lists all of the goals the user has set."""

	user = model.get_user_by_email(flask_session["email"])

	goals = user.goals

	return render_template("goal_log.html" , goals = goals, goal_dictionary = model.goal_dictionary)

@app.route("/new_goal")
def new_goal():
	"""Renders the form the user completes to add a goal."""
	return render_template("new_goal.html")

@app.route("/race_search")
def race_search():
	goal = request.args.get("goal")
	zipcode = request.args.get("zipcode")
	# Right now I am searching near the given zipcode, 
	# but I might let the user search by city, etc.
	# city = request.args.get("city")
	# state =request.args.get("state")
	# location = ""
	# for letter in city:
	# 	if letter == " ":
	# 		location = location + "%20"
	# 	else:
	# 		location = location + letter
	# location = location + "," + state.upper() + ",US"
	# print location
	fitness = int(request.args.get("fitness_level"))
	run_length_history = int(request.args.get("run_length_history"))
	# Base date is the date that the goal is being made. The date
	# range for the race search is based on when the goal is created. 
	base_date = date.today()
	# Date range returns a tuple a minimum number of weeks
	# in the future to look for a date and a maximum number of weeks. 
	date_range = goals.determine_date_range(goal, fitness, run_length_history)
	# min_date is the earliest to look for a race. 
	min_date = base_date + timedelta(date_range[0]*7)
	# max date is the latest to look for a race. 
	max_date = base_date + timedelta(date_range[1]*7)

	# print str(min_date), str(max_date)

	# Setting up and executing the API call.
	print "Getting ready to call the API"
	# I decided to go with quality data over quantity.
	# URL will only return results that have a url associated with the organizer.
	activity_request_url = "http://api.amp.active.com/v2/search?attributes=" + model.distance_dictionary[goal] + "&category=event&start_date=" + str(min_date) +".."+str(max_date)+"&near="+str(zipcode)+ "&exists=homePageUrlAdr&api_key="+ACTIVEDOTCOM_KEY
	activity_request = requests.get(activity_request_url)
	print "Active.com API request ran."
	# json_output = activity_request.json()
	# print json_output
	# print activity_request.content
	content = activity_request.content
	content_dictionary = json.loads(content)
	# print content_dictionary
	results = content_dictionary[u'results']
	unique_content = []

	for i in range(len(results)-1):
		do_not_append_content = False
		for j in range(i + 1, len(results)):
			if results[i]['homePageUrlAdr'] == results[j]['homePageUrlAdr']:
				do_not_append_content = True
			else:
				pass

		print do_not_append_content
		if do_not_append_content == True:
			pass
		else:
			unique_content.append(results[i])
 	print unique_content
 	json_content = json.dumps(unique_content)	
	return json_content

@app.route("/add_goal", methods=["POST"])
def add_goal():
	"""Adds a goal to the database when the user submits the new goal form."""
	user = model.get_user_by_email(flask_session["email"])
	goal = request.form.get("goal")
	fitness_level = request.form.get("fitness_level")
	run_length_history = request.form.get("run_length_history")
	set_date = date.today()
	race_data = request.form.get("race")
	race_data = json.loads(race_data)
	race_url = str(race_data[0])
	event_date = datetime.strptime(str(race_data[1]), "%Y-%m-%dT%H:%M:%S.%fZ")
	id_for_api = str(race_data[2])

	print race_data

	new_goal = model.Goal(user_id = user.id, description=goal, fitness_level=fitness_level, run_length_history=run_length_history, set_date=set_date, race_url = race_url, event_date = event_date, id_for_api = id_for_api)

	model.insert_new_goal(new_goal)

	return redirect("/goals")

@app.route("/view_goal.html")
def view_goal():
	"""Views a goal that the user previously set."""
	current_goal_id = request.args.get("goal_id")
	current_goal = model.get_goal_by_id(current_goal_id)
	return render_template("view_goal.html", goal=current_goal, goal_dictionary = model.goal_dictionary)

@app.route("/mood_map_after")
def after_mood():
	user = model.get_user_by_email(flask_session["email"])

	number_of_runs = request.args.get("number_of_runs")

	after_rating_list = model.get_after_ratings(user, runs_to_get = number_of_runs)

	print after_rating_list

	feelings_ratings = {"name": "Root", "children": [{"name": "After Run", "children": [], "size": 800}], "size": 1000}
	
	for i in range (len(after_rating_list)):
		feelings_ratings["children"][0]["children"].append({"name": str(after_rating_list[i][0]), "size": after_rating_list[i][1], "score": after_rating_list[i][0]})

	# print feelings_ratings
	json_feelings = json.dumps(feelings_ratings)
	return json_feelings

@app.route("/mood_map_before")
def before_mood():
	user = model.get_user_by_email(flask_session["email"])

	number_of_runs = request.args.get("number_of_runs")

	if number_of_runs == None:
		number_of_runs = 5

	before_rating_list = model.get_before_ratings(user, runs_to_get = number_of_runs)

	print before_rating_list

	feelings_ratings = {"name": "Root", "children": [{"name": "Before Run", "children": [], "size": 800}], "size": 1000}
	
	for i in range (len(before_rating_list)):
		feelings_ratings["children"][0]["children"].append({"name": str(before_rating_list[i][0]), "size": before_rating_list[i][1]})
	
	# print feelings_ratings
	json_feelings = json.dumps(feelings_ratings)
	return json_feelings


@app.route("/mood_map_during")
def flare_data():
	user = model.get_user_by_email(flask_session["email"])

	number_of_runs = request.args.get("number_of_runs")

	if number_of_runs == None:
		number_of_runs = 5

	during_rating_list = model.get_during_ratings(user, runs_to_get = number_of_runs)

	print during_rating_list

	feelings_ratings = {"name": "Root", "children": [{"name": "During Run", "children": [], "size": 800}], "size": 1000}
	
	for i in range (len(during_rating_list)):
		feelings_ratings["children"][0]["children"].append({"name": str(during_rating_list[i][0]), "size": during_rating_list[i][1]})
	
	
	# print feelings_ratings
	json_feelings = json.dumps(feelings_ratings)
	return json_feelings

# These Routes are for logging you out. 

@app.route("/sign_out")
def end_session():

	flask_session.clear()

	return redirect("/")







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)