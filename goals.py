# This is where I am going to include some of 
# the logic around which the app decides the date range
# in which to search for a goal race. It is here because
# I do not want to make my controller file overly messy. 

def determine_date_range(goal, fitness, run_length_history):
	"""This function will help establish a date range to 
	search for an appropriate race given the user inputed info."""

	if goal == "run_walk_5k":
		
		if fitness < 3 and run_length_history == 1:
			weeks = 10 
		elif fitness < 3 and run_length_history < 3:
			weeks = 9
		elif fitness < 3:
			weeks = 8

		else:
			weeks = 6

	elif goal == "run_5k":
		
		if fitness < 3 and run_length_history == 1:
			weeks = 14
		elif fitness < 3 and run_length_history < 3:
			weeks = 12
		elif fitness < 3:
			weeks = 10
		elif fitness < 8:
			weeks = 8 
		else:
			weeks = 6

	elif goal == "run_walk_10k":
		
		if fitness < 3 and run_length_history == 1:
			weeks = 16
		elif fitness < 3 and run_length_history < 3:
			weeks = 14
		elif fitness < 3:
			weeks = 12
		elif fitness < 8:
			weeks = 8 
		else:
			weeks = 6

	elif goal == "run 10k":

		if fitness < 3 and run_length_history == 1:
			weeks = 20
		elif fitness < 3 and run_length_history < 3:
			weeks = 18
		elif fitness < 3:
			weeks = 16
		elif fitness < 8:
			weeks = 10 
		else:
			weeks = 8

	elif goal == "run_walk_half":
		if fitness < 3 and run_length_history == 1:
			weeks = 24
		elif fitness < 3 and run_length_history < 3:
			weeks = 22
		elif fitness < 3:
			weeks = 18
		elif fitness < 8:
			weeks = 12 
		else:
			weeks = 10


	# goal == "run_half"

	else:
		if fitness < 3 and run_length_history == 1:
			weeks = 32
		elif fitness < 3 and run_length_history < 3:
			weeks = 26
		elif fitness < 3:
			weeks = 22
		elif fitness < 8:
			weeks = 16 
		else:
			weeks = 14

# Add options for full marathons if I decide that 
# isn't crazy. 
	week_range = (weeks-1, weeks + 5)

	return week_range
