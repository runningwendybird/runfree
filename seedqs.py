#This is the file I will use to see the question table in the database. 

import model

pre_run = model.Question(question="How did you feel before the run?: ", minimum = 0, maximum =5)
during_run = model.Question(question="How did you feel during the run?: ", minimum = 0, maximum =5)
post_run = model.Question(question="How did you feel after the run?: ", minimum = 0, maximum =5)
energy = model.Question(question="How would you rate your energy today?: ", minimum = 0, maximum =5)
feeling = model.Question(question="Select a word to describe how you are feeling: ")
location = model.Question(question="Select a word to describe where you ran: ")
terrain = model.Question(question="Select a word to describe the terrain: ")
route = model.Question(question="Select a word to describe the route you ")
thoughts = model.Question(question="Any additional thoughts? ")

questions = [pre_run, during_run, post_run, energy, feeling, location, terrain, route, thoughts]

def seed(question_list):
	for question in question_list:
		model.sqla_session.add(question)

	model.sqla_session.commit()

