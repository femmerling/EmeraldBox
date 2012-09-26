#!flask/bin/python
from migrate.versioning import api
import imp
#import logging
import sys
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

def db_create():
	db.create_all()
	if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		api.create(SQLALCHEMY_MIGRATE_REPO,'database repository')
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print 'Database creation completed'
	else:
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, lastversion)

def db_migrate():
	migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	exec old_model in tmp_module.__dict__
	script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
	open(migration, "wt").write(script)
	a = api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print 'New migration saved as ' + migration
	print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def db_upgrade():
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print 'Database upgrade completed!'
	print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def db_downgrade(version=None):
	if not version:
		current_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		downgrade_version = current_version - 1
	else:
		downgrade_version = version
	api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, downgrade_version)
	print 'Database downgrade completed!'
	print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def help():
	print '\nThe general usage pattern of the tool is python db_tools.py [options]\n'
	print 'The following are the available options:\n'
	print '--create or -c 			: Create the database for the first usage. Only use this if you want to create the database for the first time'
	print '--migrate or -m 		: Create the migration script for migration process'
	print '--upgrade or -u 		: Upgrade the database to the latest migration version'
	print '--downgrade or -d 		: Downgrade the databse to the previous migration version.'
	print '				  To downgrade to a specific version use python db_tools.py -d [version number]'
	print '--help or -h 			: Display the help file'


def db_version():
	current_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print 'The current database version is ' + current_version


#sysinput = sys.argv
#print sys.argv
sysinput = sys.argv[1].lower()
if sysinput == '--help' or sysinput == '-h':
	help()
elif sysinput == '--create' or sysinput == '-c':
	if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		db_create()
	else:
		print 'Previous database version found. Please use -m or --migrate option'
elif sysinput == '--migrate' or sysinput == '-m':
	db_migrate()
elif sysinput == '--upgrade' or sysinput == '-u':
	db_upgrade()
elif sysinput == '--downgrade' or sysinput == '-d':
	if len(sys.argv) > 2 and sys.argv[2].isdigit():
		db_downgrade(sys.argv[2])
	else:
		db_downgrade()