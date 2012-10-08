# Description

EmeraldBox is a boilerplate framework for developing python web applications with database access. 
The framework is based on Flask, a python microframework based on werkzeug, jinja2 and good intentions.
Several basic packages commonly used in developing web applications are included.
EmeraldBox also provides a structure to Flask applications since currently there are no standardized approach to structuring applications.

# Motivation
Currently there are no complete all in one package available that includes common packages for developing web applications using Flask on a non-GAE platform.
Therefore I set this repo up with packages that I'll use on my projects.
The tool includes database management tools based on SQLAlchemy and is designed to give ease for developers in managing database and migrations. I implement a more rails-like approach since it helps developers in many ways.

# Installed packages

Currently the following packages are included.
* Flask
* Flask Mail
* Flask WTF
* Flask SQLAlchemy
* Python MySQL
* SQLAlchemy Migrate
* Markdown
* Migrate
* Flup
* PIL

You can add your desired package by running:

    flask/bin/pip install <package name>

# Setup

clone repository

    git clone https://github.com/femmerling/EmeraldBox.git <project_name>

change to directory of <project_name>

    cd <project_name>

add replace remote

    git remote rm origin
    git remote add origin <new_remote like git@github.com:your_name/project_name.git>
    git commit -am "initial setup"
    git push origin master

EmeraldBox is a localized environment build using virtualenv.
To adjust the environment settings to your local environment, go to the root EmeraldBox directory and run:

	python setup.py

# Usage

run the server using:
		
	./ignite.py

Framework generators and tools available. to see the functions run:

	./box.py -h

Automated database creation tool available.

Run the following:

    ./box.py -n <Model Name> <field name>:<field type>--<field length (optional)>

Afterwards run:

    ./box.py -m

Your database will then be migrated and create the tables in the database. This also creates a controller in your controller file for handling the JSON output of your model.
Check app/main.py to see the result.

if you have an empty model, the new database will be created. If you are adding a new model run the following after the -n function is executed:

    ./box.py -m
    ./box.py -u

You can also initiate your own controller in the controller file.
Simply run the following

    ./box.py -i <controller name>

# Other Notes

Currently no documentation is available and the project is at its early alpha. Use carefully.

for documentation on python see http://www.python.org <br>
for documentation on Flask see http://flask.pocoo.org <br>
for documentation on SQLAlchemy see http://www.sqlalchemy.org <br>

If you found any issues please put them in the issue section. I'll respond to it as soon as I have time.

for direct contact email erich@emfeld.com


