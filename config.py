import os  # << uncomment for SQLAlchemy Migrate Usage
basedir = os.path.abspath(os.path.dirname(__file__))  # << uncomment for SQLAlchemy Migrate Usage

#CSRF_ENABLED = True
#SECRET_KEY = 'j;wD=R#2]07l65r+J)9,%)D[f:1,VS.+RQ+5VY.]lP]\wY:K' << use your own key, this is just an example

#SQLALCHEMY_DATABASE_URI = 'mysql://root:password01@127.0.0.1/flasklearn' # << use this for MySQL, adjust accordingly
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/app.db')  # << use this for SQLite, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost/mydatabase' #<< use this for postgresql, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'oracle://scott:tiger@127.0.0.1:1521/sidname' #<< use this for oracle, adjust accordingly

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # << if you want to use SQLAlchemy Migrate
