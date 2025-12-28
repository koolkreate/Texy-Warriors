from flask import Blueprint

# Create a blueprint for the routes
main = Blueprint('main', __name__)

# Import routes here
from . import example_routes  # Assuming you will create example_routes.py for specific routes