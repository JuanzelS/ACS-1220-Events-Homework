"""Initialize the Flask application."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Use absolute path for the database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# Import models first to ensure they're registered with SQLAlchemy
from events_app.models import Guest, Event

# Import the routes AFTER creating the app and db objects
from events_app.routes import main

# Register the blueprint
app.register_blueprint(main)