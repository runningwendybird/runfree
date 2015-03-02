# This file should be run in order to seed the
# database with run/rating information. Runs can also be
# added to the database by filling out a form, but
# this will be a faster way of seeding the database with
# dozens of runs at once. 

import model
import random
import datetime

def seedruns(user_id, number_of_runs_to_add, starting_date, run_id_start):

	count = 0

	zipcode_choices = ['92126', '93711', '94577', '93720']
	distance_choices = [1.5, 2, 5, 7, 9, 10, 4, 3.1, 6.2, 13.1, 2.25, 8]
	time_choices = [20, 25, 50, 75, 100, 110, 45, 45, 120, 200, 35, 90]

	run_id = run_id_start

	for run in range(number_of_runs_to_add - 1):
		
		# Will add a run object to the sqlalchemy session. 
		user_id = user_id
		date_run = starting_date + datetime.timedelta(count) 
		zipcode = random.choice(zipcode_choices)
		approx_dist = random.choice(distance_choices)
		approx_time = time_choices[distance_choices.index(approx_dist)]

		current_run = model.Run(user_id = user_id, id = run_id, date_run = date_run, zipcode = zipcode, approx_dist = approx_dist, approx_time = approx_time)
		model.sqla_session.add(current_run)

		# will add ratings for the recently added run object. 

		for question_id in range (1, 10):
			# For number ratings

			if question_id == 1:
				random_rating_number = random.choice([1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			if question_id == 2:
				random_rating_number = random.choice([1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			if question_id == 3:
				random_rating_number = random.choice([1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			if question_id == 4:
				random_rating_number = random.choice([1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5])
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, numeric_ans = random_rating_number)

			# For selection ratings. 

			if question_id == 5:
				feeling_choices = ['positive', 'optimistic', 'refreshed', 'excited', 'peaceful', 'nervous', 'upset', 'ill', 'injured', 'tired']
				random_feeling = random.choice(feeling_choices)
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_feeling)
			
			if question_id == 6:
				location_choices = ['park', 'city', 'neighborhood', 'trail', 'beach', 'track', 'treadmill']
				random_location = random.choice(location_choices)
				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_location)
				# Creating a location rating in order to make sure if treadmill is selected
				# that the treadmill will be consistent throughout ratings.
				location_rating = current_rating
			
			if question_id == 7:
				terrain_choices = ['flat', 'downhill', 'uphill', 'hills']
				
				# checking track for consistency. 
				
				if location_rating.select_ans == "track":
					random_terrain = "flat"
				else:
					random_terrain = random.choice(terrain_choices)

				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_terrain)
			
			if question_id == 8:
				route_choices = ['out_and_back', 'point_to_point', 'random', 'track']

				# Checking treadmill for consistency. 

				if location_rating.select_ans == "treadmill":
					random_route = "treadmill"
				else:
					random_route = random.choice(route_choices) 


				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, select_ans = random_route)

			if question_id == 9:

				dummy_text = ["What a good run! I am a beast!", 
				"Tired in the beginning, but improved about a mile in.", 
				"Just what I needed today.", 
				"Today was a hard run.", 
				"I can't wait for my upcoming race!", 
				"Feeling tired this week.", 
				"Burned off stress. Huzzah!", 
				"Legs are tired, heart and lungs felt strong!", 
				"Best part of my day", 
				"I can't wait to run again."]

				random_text = random.choice(dummy_text)

				current_rating = model.Rating(user_id = user_id, run_id = run_id, question_id = question_id, text_ans = random_text)

			model.sqla_session.add(current_rating)

		count = count + 1
		run_id = run_id + 1

	model.sqla_session.commit()
	print "Commited runs and ratings to the database."

def select_start_date():
	print "This will select a start date to generate from."
	
	day_of_month = int(input("Enter day of the month in DD format: "))
	month = int(input("Enter the month in MM format: "))
	year = int(input("Enter the year YYYY format: "))

	starting_date = datetime.datetime(year, month, day_of_month, 8, 45, 0, 0)

	return starting_date

def main():

	# Set up all the parameters we need to start the seeding. 

	starting_date = select_start_date()
	user_id = int(input("Enter user_id for whom you want to add runs: "))
	number_of_runs_to_add = int(input("Enter number of runs to add."))
	run_id_start = int(input("Enter desired starting run_id: "))

	# Seed the database. 

	seedruns(user_id, number_of_runs_to_add, starting_date, run_id_start)


if __name__ == "__main__":
	main()

		