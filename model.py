# This is my model file. My class definitions, reused functions, 
# etc. will live here. 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import date
from datetime import datetime

ENGINE = create_engine("sqlite:///runfree.db", echo=True)
sqla_session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = sqla_session.query_property()


#
# Classes
#

class User(Base):

	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), unique = True, nullable = False)
	password = Column(String(64), nullable = True)
	first = Column(String(64), nullable = True)
	last = Column(String(64), nullable = True)
	birthdate = Column(DateTime(timezone = False), nullable = True)
	sex = Column(String(15), nullable = True)
	zipcode = Column(String(15), nullable = True)

	runs = relationship("Run", backref=backref("user"))
	goals = relationship("Goal", backref=backref("user"))
	

	def __repr__(self):
		return "User with email: %s" % self.email

class Run(Base):

	__tablename__ = "runs"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey("users.id"))
	date_run = Column(DateTime(timezone = False), unique = True, nullable = True)
	zipcode = Column(String(16), nullable = True)
	approx_dist = Column(Float, nullable = True)
	approx_time = Column(Integer, nullable = True)

	ratings = relationship("Rating", backref=backref("run"))
 
	def __repr__(self):
		return "Run on %s" % datetime.strptime((str(self.date_run)), "%Y-%m-%d %H:%M:%S").strftime("%m-%d-%Y")

class Question(Base):

	__tablename__ = "questions"

	id = Column(Integer, primary_key = True)
	question = Column(String(200), nullable = False)
	minimum = Column(Integer, nullable = True)
	maximum = Column(Integer, nullable = True)

	def __repr__(self):
		return "%s" % self.question

class Rating(Base):

	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey("users.id"))
	run_id = Column(Integer, ForeignKey("runs.id"))
	question_id = Column(Integer, ForeignKey("questions.id"))
	numeric_ans = Column(Integer, nullable = True)
	select_ans = Column(String(100), nullable = True)
	text_ans = Column(Text, nullable = True)

	def __repr__(self):
		return "User ID: %d, Run ID: %d, Question ID: %d" % (self.user_id, self.run_id, self.question_id)

class Goal(Base):

	__tablename__ = "goals"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey("users.id"))
	description = Column(String(200), nullable = False)
	fitness_level = Column(String(200))
	run_length_history = Column(String(15))
	set_date = Column(DateTime(timezone = False), nullable = False)
	race = Column(Boolean)
	zipcode = Column(String(15))
	radius = Column(Integer)

	def __repr__(self):
		return "User: %d, Goal: %s" % (self.user_id, self.description)



# Eventually I want to help the user determine appropriate
# steps to take in order to complete their goal. This could
# be a "nice to have" feature after I complete my MVP.


# class Subgoal(Base):

# 	__tablename__ = "milestones"

# 	id = Column(Integer, primary_key = True)
# 	goal_id = Column(Integer, ForeignKey("goals.id"))
# 	description = Column(String(200), nullable = True)
# 	date = Column(DateTime(timezone = False), nullable = True)
# 	url = Column(String(300), nullable = True)
# 	date_completed = Column(DateTime(timezone = False), nullable = True)

# 	goal = relationship("Goal", backref=backref("subgoals", order_by = id))
	
# 	def __repr__(self):
# 		return "%s" % self.subgoal


# -----------Classes End--------------------------

#
# functions
#

def insert_new_user(new_user):
	
	"""Will insert a new user into the database when he
	or she signs up."""
	sqla_session.add(new_user)
	sqla_session.commit()

def get_user_by_email(email):
	"""Returns the user object associated with an email address."""
	
	user = sqla_session.query(User).filter_by(email=email).one()
	
	return user

def insert_new_run(new_run):
	"Will insert a new run into the database for the user."
	sqla_session.add(new_run)
	sqla_session.commit()

def get_run_by_datetime(datetime_obj):
	"""Will find a run with a particular time stamp."""
	run = sqla_session.query(Run).filter_by(date_run=datetime_obj).first()

	return run

def get_run_by_id(run_id):
	"""Will find a run with the indicated run_id."""
	run = sqla_session.query(Run).filter_by(id=run_id).first()

	return run

def find_all_runs(user):
	"""Returns a list of all the users runs"""

	runs = sqla_session.query(Run).filter_by(user_id = user.id).all()

	return runs

def insert_new_goal(new_goal):
	"""Will insert a new goal into the database."""
	sqla_session.add(new_goal)
	sqla_session.commit()



def create_db():
	"""Recreates the database."""

	Base.metadata.create_all(ENGINE)

