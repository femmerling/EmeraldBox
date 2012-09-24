from flask import render_template
from app import app

# define global variables here

@app.route('/')
def index():
	# define your controller here
	return 'Hello World'