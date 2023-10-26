# Import necessary modules
import os
from flask import Flask
from application import config 
from application.config import LocalDevelopmentConfig
from application.database import db

# Initialize the 'app' variable to None
app = None

# Define a function to create the Flask application
def create_app():
    # Create a Flask app instance, specifying the template folder
    app = Flask(__name__, template_folder='templates')

    # Check the value of the 'ENV' environment variable; default to 'development' if not set
    if os.getenv('ENV', "development") == 'production':
        # Raise an exception if the environment is set to 'production' (no production config is set up)
        raise Exception("Currently no production config is setup")
    else:
        # Print a message indicating that the local development environment is starting
        print('Starting Local Development')
        # Load configuration settings from the LocalDevelopmentConfig class
        app.config.from_object(LocalDevelopmentConfig)
    
    # Initialize the database with the Flask app instance
    db.init_app(app)

    # Push the application context onto the Flask app
    app.app_context().push()
    
    # Return the configured Flask app
    return app

# Create the Flask app using the 'create_app' function
app = create_app()

# Set a secret key for the Flask app (used for session management)
app.secret_key = "very secret"

# Import controllers for the application
from application.controllers import *

# Run the Flask app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
