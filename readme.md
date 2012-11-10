# Description

EmeraldBox is a boilerplate framework for developing python web applications with database access. 
The framework is based on Flask, a python microframework based on werkzeug, jinja2 and good intentions.
Several basic packages commonly used in developing web applications are included.
EmeraldBox also provides a structure to Flask applications based on Flask's best practice for large applications. However, EmeraldBox did not implement Blueprint.

The structure implemented is mostly based on the following links:
* http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world by Miguel Grinberg
* http://flask.pocoo.org/docs/patterns/packages/ by Armin Ronacher

# Motivation
Currently there are no complete all in one package available that includes common packages for developing web applications using Flask on a non-GAE platform.
Therefore this repo is set with the most common packages used in a standard web development project.
The tool includes database management tools based on SQLAlchemy and is designed to give ease for developers in managing database and migrations. A more rails-like approach is used since it helps developers in many ways.

# Installer package

EmeraldBox setup will install the following packages for you:
* Flask
* Flask-Mail
* Flask-SQLAlchemy
* SQLAlchemy
* SQLAlchemy-Migrate
* Nose
* Tornado Web Server

You can add your desired package by running:

    box/bin/pip install <package name>

# Setup

clone repository

    git clone https://github.com/femmerling/EmeraldBox.git <project_name>

EmeraldBox is a localized environment build using virtualenv.
To adjust the environment settings to your local environment, go to the root EmeraldBox directory and run:

    python setup.py

The setup will then automatically download packages and adjusted your settings.

If you want to control your project using git do the followings:

change to directory of <project_name>

    cd <project_name>

add replace remote

    git remote rm origin
    git remote add origin <new_remote like git@github.com:your_name/project_name.git>
    git commit -am "initial setup"
    git push origin master

# Server and Deployment

As all python frameworks, EmeraldBox is dependent on WSGI. Worry not! EmeraldBox comes with the famous Tornado Web Server. You app is ready to be deployed and run since instalation. Run the server using:
        
    ./ignite.py

The app will run at port 5000. You can change the port in the ignite.py file to any port you wish for. Just make sure that the port is available and does not conflict with other services.

# Usage

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

this controller initiation will also automatically generate a view file in your app/templates/ folder with your controller name as the file name.

# Testing

Currently we include Nosetest into the package. You can use it to perform BDD.

To execute Nose, simply run the following

    box/bin/nosetests

# Other Notes

Currently no documentation is available and the project is at its early alpha. Use carefully.

for documentation on python see http://www.python.org <br>
for documentation on Flask see http://flask.pocoo.org <br>
for documentation on SQLAlchemy see http://www.sqlalchemy.org <br>

If you found any issues please put them in the issue section. I'll respond to it as soon as I have time.

for direct contact email erich@emfeld.com

