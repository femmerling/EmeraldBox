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
	print '\nThe general usage pattern of the tool is python db_tools.py [options] [extra parameters]\n'
	print 'The following are the available options:\n'
	print '	--create or -c 			: Create the database for the first usage. Only use this if you want to create the database for the first time'
	print '	--migrate or -m 		: Create the migration script for migration process'
	print '	--upgrade or -u 		: Upgrade the database to the latest migration version'
	print '	--downgrade or -d 		: Downgrade the database to the previous migration version.'
	print '					  To downgrade to a specific version use python db_tools.py -d [version number]'
	print '	--new or -n 			: Create new data model.'
	print '					  The pattern is db_tools.py -n [model name] [<field name>:<field type>,<field length (if applicable. otherwise, default will be used)>]'
	print '	--help or -h 			: Display the help file'
	print ''

def add_model(model_name, model_components):
	basedir = os.path.abspath(os.path.dirname(__file__))
	model_path = os.path.join(basedir, 'app/models.py')
	#print model_name
	#print model_components
	with open(model_path, 'a') as model_file:
		model_file.write('')
		model_file.write('#test')

	#	model_file.write('\n# testline')
	print 'Model test done'


def db_version():
	current_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print 'The current database version is ' + current_version

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
elif sysinput == '--new' or sysinput == '-n':
	if len(sys.argv) > 2:
		model_name = sys.argv[2].title()
		raw_component = sys.argv[3:]
		model_components = []
		for component in raw_component:
			raw_field = component.split(':')
			field_name = raw_field[0]
			detail_components = raw_field[1].split('--')
			insert_components = {
														'field_name':field_name,
														'field_property': detail_components
													}
			model_components.append(insert_components)
		add_model(model_name,model_components)
	else:
		print 'Not enough parameters are provided. See db_tools.py -h for info'
else:
	print 'Command not found. Please use --help for command options'