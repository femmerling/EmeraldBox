# Description

EmeraldBox is a boilerplate framework for developing Flask-based web applications. 
It is based on Flask and several basic packages commonly used in developing web applications are included.
EmeraldBox also provides a structure to Flask applications since currently there are no standardized approach to structuring applications.

# Motivation
Currently there are no complete all in one package available that includes common packages for developing web applications using Flask on a non-GAE platform.
Therefore I set this repo up with packages that I'll use on my projects.
The tool includes database management tools based on SQLAlchemy and is designed to give ease for developers in managing database and migrations.

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

	python virtualenv.py flask

# Usage

run the server using:
		
	python ignite.py

db tools for migration available. to see the functions run:

	python db_tools.py -h

the above functions work on activated virtualenv. If you choose not to activate the virtualenv, use flask/bin/python to replace python.
Example:

	flask/bin/python ignite.py

Automated database creation tool available.

Run the following:

    python db_tools.py -n <Model Name> <field name>:<field type>--<field length (optional)>

Afterwards run:

    flask/bin/python db_tools.py -m

Your database will then be migrated and create the tables in the database.

if you have an empty model, the new database will be created. If you are adding a new model run the following after the -n function is executed:

    python db_tools.py -m
    python db_tools.py -u


# Other Notes

Currently no documentation is available and the project is at its early alpha. Use carefully.

for documentation on python see http://www.python.org <br>
for documentation on Flask see http://flask.pocoo.org <br>
for documentation on SQLAlchemy see http://www.sqlalchemy.org <br>

If you found any issues please put them in the issue section. I'll respond to it as soon as I have time.

for direct contact email erich@emfeld.com


