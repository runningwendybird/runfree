# This is my model file. My class definitions, reused functions, 
# etc. will live here. 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

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
	email = Column(String(64), nullable = False)
	password = Column(String(64), nullable = True)

	# def __repr__(self):
	# 	return "User with email: %s" % self.email

	# def get_user_by_email(self, email):
	# 	"""Returns the user object associated with an email address."""
		
	# 	user = sqla_session.query(User).filter_by(email=email).one()
		
	# 	return user

# -----------Classes End--------------------------

#
# functions
#



def insert_new_user(new_user):
	"""Will insert a new user into the database when he
	or she signs up."""
	sqla_session.add(new_user)
	sqla_session.commit()



