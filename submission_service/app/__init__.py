from flask import Flask

app = Flask(__name__)

# Import the routes to ensure they are registered with the app
from . import submit_service
