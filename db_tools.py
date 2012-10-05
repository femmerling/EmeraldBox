#!flask/bin/python
import imp
import sys
import os.path

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db

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

def db_create():
	db.create_all()
	if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		api.create(SQLALCHEMY_MIGRATE_REPO,'database repository')
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print '\nDatabase creation completed\n'
	else:
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def db_migrate():
	migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	exec old_model in tmp_module.__dict__
	script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
	open(migration, "wt").write(script)
	a = api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print 'New migration saved as ' + migration
	print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)) + '\n'

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

def add_model(model_name, model_components):
	basedir = os.path.abspath(os.path.dirname(__file__))
	model_path = os.path.join(basedir, 'app/models.py')
	model_file = open(model_path, 'a')
	model_file.write('\n')
	model_file.write('class ' + model_name + '(db.Model):\n')
	model_file.write('	id = db.Column(db.BigInteger, primary_key=True)\n')
	
	for component in model_components:
		in_type = component['field_property'][0].lower()
		if in_type == 'string':
			data_type = 'String'
		elif in_type == 'text':
			data_type = 'Text'
		elif in_type == 'integer':
			data_type = 'Integer'
		elif in_type == 'biginteger':
			data_type = 'BigInteger'
		elif in_type == 'float':
			data_type = 'Float'
		elif in_type == 'boolean':
			data_type = 'Boolean'
		elif in_type == 'binary':
			data_type = 'Binary'
		else:
			print 'Data type ' + component['field_property'][0] + ' not found. Please refer to SQLAlchemy documentation for valid data types.'
			sys.exit()

		if len(component['field_property']) == 2:
			model_file.write('	' + component['field_property'][0].lower() + ' = db.Column(db.'+ data_type + '('+ component['field_property'][1] +'))\n')
		else:
			model_file.write('	' + component['field_property'][0].lower() + ' = db.Column(db.'+ data_type + ')\n')

	model_file.write('	def dto(self):\n')
	model_file.write('		return dict(\n')
	mod_counter = 1
	max_mod_index = len(model_components)
	for component in model_components:
		mod_counter = mod_counter + 1
		if mod_counter != max_mod_index:
			model_file.write('				' + component['field_property'][0].lower() + ' = self.'+ component['field_property'][0].lower() + '\n')
		else:
			model_file.write('				' + component['field_property'][0].lower() + ' = self.'+ component['field_property'][0].lower() + ',\n')
	model_file.write('			)')
	model_file.write('')
	model_file.close()
	print '\n...........\n'
	print 'Database file is ready to use.\nRun python db_tools.py -c if you want to initialize the database or run python db_tools.py -m if this is a migration.\n'

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
		print '\nPrevious database version found. Please use -m or --migrate option\n'
		sys.exit()
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
		valid_data_types = ['string','text','integer','biginteger','float','boolean','binary']
		if raw_component:
			model_components = []
			for component in raw_component:
				raw_field = component.split(':')
				field_name = raw_field[0]
				detail_components = raw_field[1].split('--')
				if detail_components[0].lower() == 'string':
					if len(detail_components) < 2:
						print 'String data type requires length. Please refer to -h.'
						sys.exit()
				insert_components = {
															'field_name':field_name,
															'field_property': detail_components
														}
				model_components.append(insert_components)
		else:
			print '\nNot enough parameters are provided. Model requires field definitions. See db_tools.py -h for info\n'
			sys.exit()
		add_model(model_name,model_components)
	else:
		print '\nNot enough parameters are provided. See db_tools.py -h for info\n'
else:
	print '\nCommand not found. Please use --help for command options\n'



# end of file