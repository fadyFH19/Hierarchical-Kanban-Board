# Import the necessary modules to work with SQLAlchemy and Flask-SQLAlchemy.
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

# Create a variable 'engine' which is currently set to None.
engine = None

# Create a declarative base class for defining database models using SQLAlchemy.
Base = declarative_base()

# Create a SQLAlchemy database object, often used to interact with the database.
db = SQLAlchemy()
