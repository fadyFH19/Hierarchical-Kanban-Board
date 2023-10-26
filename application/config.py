# Import the 'os' module for working with file paths and directories.
import os

# Get the absolute path of the directory containing this Python script.
basedir = os.path.abspath(os.path.dirname(__file__))

# Create a base configuration class.
class Config():
    # Set the DEBUG mode to False by default.
    DEBUG = False
    # Initialize the SQLITE_DB_DIR, SQLALCHEMY_DATABASE_URI, and SQLALCHEMY_TRACK_MODIFICATIONS to None.
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create a configuration class for local development, inheriting from the base 'Config' class.
class LocalDevelopmentConfig(Config):
    # Set the SQLITE_DB_DIR to a directory named 'db_directory' located one level above the script's directory.
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    # Set the SQLALCHEMY_DATABASE_URI to use a SQLite database file located in the 'SQLITE_DB_DIR'.
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "appdb.db")
    # Enable DEBUG mode for local development.
    DEBUG = True
