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
import time
import HTMLParser



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
	page = "landing"
	return render_template("landing.html", page = page)

@app.route("/about")
def about_runfree():
	page = "about"
	return render_template("about_runfree.html", page = page)

@app.route("/business")
def display_business_info():
	page = "business"
	return render_template("business_card.html", page = page)


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

	return redirect("/user_landing")

@app.route("/new_user")
def add_user():
	"""Sends the user to the sign up form."""
	page = "new_user"
	return render_template("new_user.html", page = page)

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

	return redirect("/user_landing")

# These Routes are for navigating the functionality 
# of the app once you are logged in. 

# These routes are to view and create runs. 

@app.route("/user_landing")
def dashboard():
	"""Displays relevant info for the user, that he or she will
	see upon logging in."""

	user = model.get_user_by_email(flask_session["email"])
	

	runs = model.get_collection_of_runs(user.id, runs_to_get = 6)
	instagrams = []
	for run in runs:
		instagram = model.get_instagram(run[3])
		if len(instagram[0].text_ans) > 20:
			instagrams.append(instagram[0].text_ans)

	#looks for more instagrams if the first search didn't return very many
	if len(instagrams) < 4:
		instagrams = []
		runs = model.get_collection_of_runs(user.id, runs_to_get = 10)
		for run in runs:
			instagram = model.get_instagram(run[3])
			if len(instagram[0].text_ans) > 20:
				instagrams.append(instagram[0].text_ans)

	if len(instagrams) > 6:
		instagrams = instagrams[:6]


	#gets outstanding subgoals 

	outstanding_subgoals = model.get_outstanding_subgoals(user)

	possible_matches = []

	for subgoal in outstanding_subgoals:
		runs_after_date = model.get_runs_after_date(user, subgoal.goal.set_date)
		for run in runs_after_date:
			if run.approx_dist >= model.distance_int_dictionary[subgoal.description]:
				possible_matches.append((subgoal, run))



	page = "user_landing"	

	return render_template("user_landing.html", instagrams=instagrams, possible_matches = possible_matches, goal_dictionary = model.goal_dictionary, page = page)

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

		runs = model.find_all_runs_desc(user)

		number_of_runs = len(runs)

		page = "run"

		return render_template("run_log.html", user = user, runs = runs, page = page, number_of_runs = number_of_runs)

@app.route("/new_run")
def new_run():
	"""Renders the form the user completes to add a run."""
	page = "run"
	user = model.get_user_by_email(flask_session["email"])
	routes = model.get_user_routes(user)
	return render_template("new_run.html", page = page, routes = routes)

@app.route("/add_run", methods = ["POST"])
def add_run():
	# User Object
	user = model.get_user_by_email(flask_session["email"])
	
	# Getting info from the form. 
	date_run = request.form.get("new_run_date_and_time")
	date_run = datetime.strptime(date_run, "%Y-%m-%dT%H:%M")
	zipcode = request.form.get("zipcode")
	distance = float(request.form.get("distance"))
	duration = int(request.form.get("duration"))
	route = request.form.get("route")
	pre_run = int(request.form.get("pre_run"))
	during_run = int(request.form.get("during_run"))
	post_run = int(request.form.get("post_run"))
	energy = int(request.form.get("energy"))
	feeling = request.form.get("feeling")
	location = request.form.get("location")
	terrain = request.form.get("terrain")
	route_type = request.form.get("route_type")
	thoughts = request.form.get("thoughts")
	instagram_html = request.form.get("instagram_embed")
	commit_date = datetime.now()

	if instagram_html == None:
		instagram_html = "<p></p>"

	# Creating a new run and adding it to the database.

	new_run = model.Run(user_id = user.id, date_run = date_run, zipcode=zipcode, approx_dist = distance, approx_time = duration, commit_date = commit_date, route = route)
	model.insert_new_run(new_run)
	new_run_object = model.get_latest_run(user)

	# Creating rating objects. 

	pre_run = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 1, numeric_ans = pre_run)
	during_run = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 2, numeric_ans = during_run)
	post_run = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 3, numeric_ans = post_run)
	energy = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 4, numeric_ans = energy)
	
	feeling = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 5, select_ans = feeling)
	location = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 6, select_ans = location)
	terrain = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 7, select_ans = terrain)
	route_type = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 8, select_ans = route_type)
	
	thoughts = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 9, text_ans = thoughts)
	instagram_embed = model.Rating(user_id=user.id, run_id=new_run_object.id, question_id = 10, text_ans = instagram_html)
	# Adding rating objects to database.
	ratings = [pre_run, during_run, post_run, energy, feeling, location, terrain, route_type, thoughts, instagram_embed]
	for rating in ratings:
		model.sqla_session.add(rating)

	model.sqla_session.commit()

	redirect_url = "/view_run.html?run_id=" + str(new_run_object.id)
	flash("Run Successfully added!")
	return redirect(redirect_url)

@app.route("/view_run.html")
def review_run():
	"""Allows the user to view a previous run."""
	current_run_id = request.args.get("run_id")
	current_run = model.get_run_by_id(current_run_id)
	current_ratings = model.get_ratings_for_run(current_run_id)
	
	html_parse = HTMLParser.HTMLParser()
	instagram_html = current_ratings[9]
	
	instagram_html = instagram_html.text_ans
	
	instagram_html = html_parse.unescape(instagram_html)
	
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

	score = model.get_run_score(current_run_id)

	if current_run.route == 0 or current_run.route == None:
		current_route = None
	else:
		current_route = model.get_route_by_id(current_run.route)


	#creates an edit url. 

	url = "/edit_run.html?run_id=" + str(current_run_id)

	print url

	page = "run"

	return render_template("view_run.html", run=current_run, ratings = current_ratings, terrain_dictionary = model.terrain_dictionary, route_dictionary = model.route_dictionary, score = score, color_zero = color_zero, color_one = color_one, color_two = color_two, color_three = color_three, instagram_html = instagram_html, edit_url=url, page = page, current_route = current_route)


@app.route("/edit_run.html")
def edit_run():
	run_id = request.args.get("run_id")
	run = model.get_run_by_id(run_id)

	ratings = model.get_ratings_for_run(run.id) 
	
	html_parse = HTMLParser.HTMLParser()
	instagram_html = ratings[9]
	
	instagram_html = instagram_html.text_ans
	
	instagram_html = html_parse.unescape(instagram_html)

	page = "run"

	return render_template("edit_run.html", run = run, ratings = ratings, instagram_html = instagram_html, page = page)

@app.route("/modify_run", methods = ["POST"] )
def update_run_on_database():
	# Getting all the relevant info.
	user = model.get_user_by_email(flask_session["email"]) 
	run_id = request.form.get("run_id")
	run_object = model.get_run_by_id(run_id)
	date_run = request.form.get("new_run_date_and_time")
	print date_run
	if date_run == "":
		date_run = run_object.date_run
	else:
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
	instagram_html = request.form.get("instagram_embed")

	# modifying run
	run_object.zipcode = zipcode
	run_object.approx_dist = distance
	run_object.approx_time = duration
	if date_run != " ":
		run_object.date_run = date_run
	model.sqla_session.commit()

	# Modifying ratings. 

	ratings = model.get_ratings_for_run(run_id)

	ratings[0].numeric_ans = pre_run
	ratings[1].numeric_ans = during_run
	ratings[2].numeric_ans = post_run
	ratings[3].numeric_ans = energy
	ratings[4].select_ans = feeling
	ratings[5].select_ans = location
	ratings[6].select_ans = terrain
	ratings[7].select_ans = route

	model.sqla_session.commit() 

	
	#checking to see if there are new text entries and commiting them 
	# if they have been updated. 

	instagram_html = request.form.get("instagram_embed")

	if len(instagram_html)< 20:
		pass
	else:
		ratings[9].text_ans = instagram_html

	if len(thoughts) < 2 or thoughts == None:
		pass
	else:
		ratings[8].text_ans = thoughts
	model.sqla_session.commit()
	
	redirect_url = "/view_run.html?run_id=" + str(run_id)
	flash("Run Successfully Updated!")
	return redirect(redirect_url)




# These routes are associated with the graphs. 

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

	print json_feelings

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

@app.route("/calendar_data.json")
def heat_map_data():
	user = model.get_user_by_email(flask_session["email"])

	runs = model.find_all_runs(user)

	run_dictionary = {}

	for run in runs:
		run_dictionary[(run.date_run - datetime(1970,1,1)).total_seconds()] = run.approx_dist 

	run_dictionary = json.dumps(run_dictionary)

	return run_dictionary

@app.route("/run_graphs")
def display_progress():

	"""Renders the graph page"""

	page = "data"

	return render_template("data_vis.html", page = page)



# These Routes are associated with viewing and creating goals. 


@app.route("/goals")
def set_goals():
	"""Lists all of the goals the user has set."""

	user = model.get_user_by_email(flask_session["email"])

	goals = user.goals

	page = "goals"

	return render_template("goal_log.html" , goals = goals, goal_dictionary = model.goal_dictionary, page = page)

@app.route("/new_goal")
def new_goal():
	"""Renders the form the user completes to add a goal."""
	user = model.get_user_by_email(flask_session["email"])

	page = "goals"
	return render_template("new_goal.html", user=user, page = page)

@app.route("/no_race_search")
def no_race_search():
	goal = request.args.get("goal")
	fitness = int(request.args.get("fitness_level"))
	run_length_history = int(request.args.get("run_length_history"))
	base_date = date.today()
	date_range = goals.determine_date_range(goal, fitness, run_length_history)
	# min_date is a minimum good date to set.  
	min_date = base_date + timedelta(date_range[0]*7)
	# max date is the later good date to set, so the user doesn't take it too easy.  
	max_date = base_date + timedelta(date_range[1]*7)

	min_date = datetime.strftime(min_date, "%m-%d-%Y")
	max_date = datetime.strftime(max_date, "%m-%d-%Y")

	dates = [min_date, max_date]

	json_output = json.dumps(dates)

	return json_output

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
	set_date = datetime.now()
	race_data = request.form.get("race")
	if race_data != None:
		race_data = json.loads(race_data)
		race_url = str(race_data[0])
		event_date = datetime.strptime(str(race_data[1]), "%Y-%m-%dT%H:%M:%S.%fZ")
		id_for_api = str(race_data[2])
		new_goal = model.Goal(user_id = user.id, description=goal, fitness_level=fitness_level, run_length_history=run_length_history, set_date=set_date, race_url = race_url, event_date = event_date, id_for_api = id_for_api)

	else:
		goal_date = request.form.get("goal_date_no_race")
		goal_date = datetime.strptime(goal_date, "%Y-%m-%d")
		new_goal = model.Goal(user_id = user.id, description=goal, fitness_level=fitness_level, run_length_history=run_length_history, set_date=set_date, event_date = goal_date)

	model.insert_new_goal(new_goal)

	goal_obj = model.get_most_recent_goal(user)


	# Adding subgoals

	for subgoal in model.subgoal_dictionary[goal_obj.description]:
		subgoal_to_add = model.Subgoal(goal_id = goal_obj.id, description = subgoal)
		model.insert_new_subgoal(subgoal_to_add)

	return redirect("/goals")

@app.route("/view_goal.html")
def view_goal():
	"""Views a goal that the user previously set."""
	user = model.get_user_by_email(flask_session["email"])
	current_goal_id = request.args.get("goal_id")
	current_goal = model.get_goal_by_id(current_goal_id)
	subgoals = model.get_subgoals_by_goal_id(current_goal_id)
	outstanding_subgoals = model.get_outstanding_subgoal_by_goal_id(current_goal_id)
	runs_after_date = model.get_runs_after_date(user, current_goal.set_date)

	possible_matches = []

	for subgoal in outstanding_subgoals:
		for run in runs_after_date:
			if run.approx_dist >= model.distance_int_dictionary[subgoal.description]:
				possible_matches.append((subgoal, run))



	update_button = False

	for subgoal in subgoals:
		if  not subgoal.date_completed:
			update_button = True

	days_left = (current_goal.event_date - datetime.now()).days

	page = "goals"

	return render_template("view_goal.html", goal=current_goal, goal_dictionary = model.goal_dictionary, subgoals = subgoals, update_button = update_button, days_left = days_left, possible_matches = possible_matches, page = page)

@app.route("/update_sub_goal")
def update_sub_goal():
	"""Will register a subgoal as complete."""
	user = model.get_user_by_email(flask_session["email"])
	goal_id = request.args.get("goal_id")
	# list of all subgoals associated with the goal we are viewing. 
	possible_subgoals = model.get_subgoals_by_goal_id(goal_id)

	# creating a list of subgoals to mark as completed.
	subgoal_to_commit = []

	for subgoal in possible_subgoals:
		subgoal_id = request.args.get(subgoal.description)
		# If the box is checked, it will register the subgoal as complete. 
		if subgoal_id != None:
			subgoal_obj = model.get_subgoal_by_id(int(subgoal_id))
			subgoal_obj.date_completed = datetime.now()
			model.sqla_session.commit()

	return redirect("/goals")

# These Routes are for displaying your ideal run

@app.route("/ideal_runs")
def display_ideal():
	""""Will display the conditions under which the user experiences the best runs."""
	user = model.get_user_by_email(flask_session["email"])
	page = "ideal"
	runs = model.find_all_runs(user)
	
	# Making a generalization about your running habits only makes sense after a certain number of runs. 
	# If you haven't logged a certain number of runs, it will render a template that 
	# will tell you that this functionality will appear after more runs are logged. 

	if len(runs) < 10:
		return render_template("go_run.html", page = page)

	run_dictionary = {}

	for run in runs:
		run_dictionary[run.id] = run


	# Finding user's average score and max score. 
	max_score = 0
	average_score = 0
	for run_key in run_dictionary.keys():
		run_score = model.get_run_score(run_key)
		if run_score > max_score:
			max_score = run_score
		average_score = average_score + run_score

	average_score = average_score/len(run_dictionary.keys())

	# Determining the threshold of what is a "highly rated run" for the indivual user. 

	high_rated_run_threshold = (max_score + average_score) * 0.5

	# Building the highly rated dictionary. 
	run_dictionary_high_score = {}

	for run_key in run_dictionary.keys():
		run_score = model.get_run_score(run_key)
		if run_score >= high_rated_run_threshold:
			run_dictionary_high_score[run_key] = run_dictionary[run_key]

	# Finding the average distance of highly rated runs.
	average_dist_high_rated_runs = 0

	for run_key in run_dictionary_high_score.keys():
		average_dist_high_rated_runs = average_dist_high_rated_runs + run_dictionary_high_score[run_key].approx_dist

	average_dist_high_rated_runs = average_dist_high_rated_runs / len(run_dictionary_high_score.keys())

	# Finding the average distance of all user runs. 
	average_dist_run = 0

	for run_key in run_dictionary.keys():
		average_dist_run = average_dist_run + run_dictionary[run_key].approx_dist

	average_dist_run = average_dist_run / len(run_dictionary.keys())


	# Finding the conditions that you prefer. 

	locations = []
	terrains = []
	routes = []

	for run_key in run_dictionary_high_score.keys():
		locations.append(model.get_location_by_run_id(run_key).select_ans)
		terrains.append(model.get_terrain_by_run_id(run_key).select_ans)
		routes.append(model.get_route_by_run_id(run_key).select_ans)

	
	prefered_terrain = {}

	# iterates through all the terrain conditions. 
	for key in model.terrain_dictionary.keys():
		# If the prefered terrain dictionary is empty it adds the key to it. 
		if prefered_terrain == {}:
			prefered_terrain[key] = (model.terrain_dictionary[key], terrains.count(key))
		# If the prefered terrain dictionary is not empty, it adds the terrain we are currently
		# on if they have the same counts. If the current terrain has a higher count, it replaces the
		# dictionary with one where the current key is the only key. If the count is less than 
		# what is currently in the dictionary, it moves along. 
		elif  terrains.count(key) == terrains.count(prefered_terrain.keys()[0]):
			prefered_terrain[key] = (model.terrain_dictionary[key], terrains.count(key))
					
		elif terrains.count(key) > terrains.count(prefered_terrain.keys()[0]):
			prefered_terrain = {}
			prefered_terrain[key] = (model.terrain_dictionary[key], terrains.count(key))

		else:
			pass

	
	prefered_route = {}

	# Iterates through all the route conditions.
	for key in model.route_dictionary.keys():
		# If the prefered route dictionary is empty it adds the key to it. 
		if prefered_route == {}:
			prefered_route[key] = (model.route_dictionary[key], routes.count(key))
		# If the prefered route dictionary is not empty, it adds the route we are currently
		# on if they have the same counts. If the current route has a higher count, it replaces the
		# dictionary with one where the current key is the only key. If the count is less than 
		# what is currently in the dictionary, it moves along. 
		elif routes.count(key) == routes.count(prefered_route.keys()[0]):
			prefered_route[key] = (model.route_dictionary[key], routes.count(key))
					
		elif routes.count(key) > routes.count(prefered_route.keys()[0]):
			prefered_route = {}
			prefered_route[key] = (model.route_dictionary[key], routes.count(key))

		else:
			pass


	prefered_location = {}

	# Iterates through all the location conditions.
	for key in model.location_dictionary.keys():
		# If the prefered location dictionary is empty it adds the key to it. 
		if prefered_location == {}:
			prefered_location[key] = (model.location_dictionary[key], locations.count(key))
		# If the prefered location dictionary is not empty, it adds the location we are currently
		# on if they have the same counts. If the current location has a higher count, it replaces the
		# dictionary with one where the current key is the only key. If the count is less than 
		# what is currently in the dictionary, it moves along. 
		elif locations.count(key) == locations.count(prefered_location.keys()[0]):
			prefered_location[key] = (model.location_dictionary[key], locations.count(key))
					
		elif locations.count(key) > locations.count(prefered_location.keys()[0]):
			prefered_location = {}
			prefered_location[key] = (model.location_dictionary[key], locations.count(key))

		else:
			pass



	# Determines the days of the week that tend to have your higher rated runs. 

	weekdays = []
	weekday_string_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

	# makes a list of weekdays with highly rated runs. 
	for run_key in run_dictionary_high_score.keys():
		weekdays.append(run_dictionary_high_score[run_key].date_run.weekday())

	prefered_weekday = {}

	for weekday in range(7):
		if prefered_weekday == {}:
			prefered_weekday[weekday] = weekdays.count(weekday)

		elif weekdays.count(weekday) == weekdays.count(prefered_weekday.keys()[0]):
			prefered_weekday[weekday] = weekdays.count(weekday)

		elif weekdays.count(weekday) > weekdays.count(prefered_weekday.keys()[0]):
			prefered_weekday = {}
			prefered_weekday[weekday] = weekdays.count(weekday)

		else:
			pass

	prefered_weekday_string = {}

	# creates a dictionary with a the weekdays as strings instead of 0-6. 
	for key in prefered_weekday.keys():
		prefered_weekday_string[weekday_string_list[key]] = prefered_weekday[key]

	prefered_weekday_keys = prefered_weekday.keys()
	prefered_location_keys = prefered_location.keys()
	prefered_terrain_keys = prefered_terrain.keys()
	prefered_route_keys = prefered_route.keys()

	location_image_dictionary = model.location_badges_dictionary
	terrain_image_dictionary = model.terrain_badges_dictionary
	route_image_dictionary = model.route_badges_dictionary

	weekday_image_dictionary = model.weekday_badges_dictionary

	return render_template("ideal.html", high_distance = average_dist_high_rated_runs, average_distance = average_dist_run, prefered_terrain = prefered_terrain, prefered_route = prefered_route, prefered_location = prefered_location, prefered_weekday = prefered_weekday_string, page = page, len_day = len(prefered_weekday_string), len_location = len(prefered_location), len_terrain = len(prefered_terrain), len_route = len(prefered_route), prefered_weekday_keys=prefered_weekday_keys, prefered_route_keys = prefered_route_keys, prefered_location_keys = prefered_location_keys, prefered_terrain_keys = prefered_terrain_keys, location_images = location_image_dictionary, terrain_images = terrain_image_dictionary, route_images = route_image_dictionary, weekday_images = weekday_image_dictionary)

# These routes are for adding running routes, viewing routes, etc. 

@app.route("/routes")
def view_route_library():
	"""Will display the user's collection of routes."""

	page = "route"
	user = model.get_user_by_email(flask_session["email"])

	routes = model.get_user_routes(user)
	
	return render_template("routes.html", page = page, routes = routes)


@app.route("/new_route")
def create_new_route():
	"""Will display a form for adding a new route to your collection."""

	page = "route"

	return render_template("new_route.html", page = page)

@app.route("/add_route", methods=["POST"])
def add_route_to_db():
	"""Adds the new route to the database"""

	user = model.get_user_by_email(flask_session["email"])

	# Getting info from form. 

	route_title = request.form.get("route_title")
	location_description = request.form.get("location_description")
	route_distance = request.form.get("route_distance")
	user_notes = request.form.get("user_notes")
	map_embed = request.form.get("map_embed")

	# creating a route object. 
	route = model.Route(user_id = user.id, title = route_title, location_description = location_description, notes = user_notes, distance = route_distance, html_embed = map_embed)

	# adding object to the database. 

	model.sqla_session.add(route)
	model.sqla_session.commit()
	

	flash("Added Route to Collection")

	return redirect("/routes")

@app.route("/view_route.html")
def view_user_route():
	"""Lets the user view details about a single route."""
	user = model.get_user_by_email(flask_session["email"])
	page = "route"
	current_route_id = request.args.get("route_id")
	current_route = model.get_route_by_id(current_route_id)

	return render_template("view_route.html", page = page, route = current_route)


# These Routes are for logging you out. 

@app.route("/sign_out")
def end_session():

	flask_session.clear()

	return redirect("/")







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)