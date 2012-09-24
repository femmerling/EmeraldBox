# Description

EmeraldBox is a boilerplate for developing Flask-based web applications.
Currently there are no complete all in one package available that meets my requirements for  developing web applications using Flask on a non-GAE platform.
Therefore I set this repo up with packages that I'll use on my projects.

# Installed packages

* Flask
* Flask Mail
* Flask WTF
* Flask Login
* Flask OpenID
* Flask SQLAlchemy
* Flask Babel
* Python MySQL
* SQLAlchemy Migrate
* Markdown
* Migrate
* Flup
* PIL

The package comes with a basic Brunch 0.8.1 for my HTML5 framework and a standard virualenv file.

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

# Usage

run the server using:
		
		python run.py