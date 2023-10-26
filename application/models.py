# Import necessary modules and packages
from .database import db  # Import the 'db' object from the 'database' module
from flask_login import UserMixin  # Import 'UserMixin' from 'flask_login'

# Define the Task class, which is a model for tasks in the database
class Task(db.Model):
    __tablename__ = 'Task'  # Set the table name for this model
    id = db.Column(db.Integer, primary_key=True)  # Define an integer column 'id' as the primary key
    title = db.Column(db.String(80), unique=True, nullable=False)  # Define a string column 'title'
    status = db.Column(db.String(80), nullable=False)  # Define a string column 'status'
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))  # Define a foreign key 'user_id' referencing 'User.id'
    parent_id = db.Column(db.Integer, db.ForeignKey('Task.id'), nullable=True)  # Define a nullable foreign key 'parent_id'

    # Define a relationship with the 'Task' model, creating a parent-child relationship
    parent = db.relationship('Task', remote_side=[id], backref='children', uselist=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)  # Define a string representation for the Task object

# Define the User class, which is a model for users in the database
class User(UserMixin, db.Model):
    __tablename__ = 'User'  # Set the table name for this model
    id = db.Column(db.Integer, primary_key=True)  # Define an integer column 'id' as the primary key
    username = db.Column(db.String(200), nullable=False)  # Define a string column 'username'
    password = db.Column(db.String(200), nullable=False)  # Define a string column 'password'
    tasks = db.relationship('Task', backref='user', lazy='dynamic')  # Define a relationship with the 'Task' model

    def __repr__(self):
        return "<Username: {}>".format(self.username)  # Define a string representation for the User object
