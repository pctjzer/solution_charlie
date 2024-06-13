#!/bin/bash

# Run the Flask application using Waitress
waitress-serve --host=0.0.0.0 --port=5002 app:app
