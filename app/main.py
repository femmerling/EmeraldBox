# do not change or move the following lines if you still want to use the db_tools.py auto generator
from app import app
import models

# you can freely change the lines below
from flask import render_template
from flask import json
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import abort
from flask import Response

# define global variables here

# home root controller
@app.route('/')
def index():
	# define your controller here
	return 'Hello World'