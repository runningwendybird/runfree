# This is my model file. My class definitions, reused functions, 
# etc. will live here. 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import date
from datetime import datetime

ENGINE = create_engine("sqlite:///runfree.db", echo=False)
sqla_session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = sqla_session.query_property()


#
# Classes
#

class User(Base):

	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = True)
	first = Column(String(64), nullable = True)
	last = Column(String(64), nullable = True)
	birthdate = Column(DateTime(timezone = False), nullable = True)
	sex = Column(String(15), nullable = True)
	

	def __repr__(self):
		return "User with email: %s" % self.email

class Run(Base):

	__tablename__ = "runs"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, nullable = False)
	date_run = Column(Integer, nullable = True)

	def __repr__(self):
		return "Run at %r" % (str(self.date_run))


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
	
	user = sqla_session.query(User).filter_by(email=email).first()
	
	return user

def insert_new_run(new_run):
	"Will insert a new run into the database for the user."
	sqla_session.add(new_run)
	sqla_session.commit()

def find_all_runs(user):
	"""Returns a list of all the users runs"""

	runs = sqla_session.query(Run).filter_by(user_id = user.id).all()

	return runs

def create_db():
	"""Recreates the database."""

	Base.metadata.create_all(ENGINE)

