import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

ADDITIONAL_PACKAGES = []
#additional_packages = ['flask-mail','nose']

#SQLALCHEMY_DATABASE_URI = 'mysql://root:password01@127.0.0.1/flasklearn' # << use this for MySQL, adjust accordingly
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'db/app.db')  # << use this for SQLite, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost/mydatabase' #<< use this for postgresql, adjust accordingly
#SQLALCHEMY_DATABASE_URI = 'oracle://scott:tiger@127.0.0.1:1521/sidname' #<< use this for oracle, adjust accordingly

SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')  # << if you want to use SQLAlchemy Migrate

# end of file