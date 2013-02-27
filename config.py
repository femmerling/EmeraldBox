import os
# Do not change these values!
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

# Add list of python libraries you wish to install on startup in this list
# Example:
# additional_packages = ['flask-mail','nose']
ADDITIONAL_PACKAGES = ['gunicorn']

# Select the database connectivity that you wish to use.
# THe current value defaults to sqlite
#SQLALCHEMY_DATABASE_URI = 'mysql://root:password01@127.0.0.1/flasklearn' # << use this for MySQL, adjust accordingly
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db/app.db')  # << use this for SQLite, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost/mydatabase' #<< use this for postgresql, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'oracle://scott:tiger@127.0.0.1:1521/sidname' #<< use this for oracle, adjust accordingly

# This is the default server port settings that will be used by the system
SERVER_PORT = 5000

# end of file