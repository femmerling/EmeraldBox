'''
base.py

Basic controller to serve the landing page and other model independent controllers.
Can also be used to server generic purposes.

'''

from flask import Blueprint
from flask import render_template
from flask import json
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import abort
from flask import Response

from app import db

# create home blueprint
base_view = Blueprint('base_view', __name__)

# create home routing
@base_view.route('/')
def index():
	return render_template('welcome.html')
