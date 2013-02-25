#! box/bin/python
import imp
import sys
import os.path
from subprocess import call
import platform

from migrate.versioning import api
from app import db
from config import BASEDIR, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

# This variable will be used to check the valid data types enterred by the user in box.py -n command.
valid_data_types = [
    'boolean', 'date', 'time', 'datetime', 'enum', 'interval', 'pickletype', 'schematype',
    'numeric', 'float', 'biginteger', 'smallinteger', 'smallint', 'string', 'bigint','int','integer',
    'text', 'unicode', 'unicodetext', 'binary', 'largebinary', 'blob'
]


def help():
    # This lists the commands used by the db_tools.py.
    print '\nThe general usage pattern of the tool is python box.py [options] [extra parameters]\n'
    print 'The following are the available options:\n'
    print ' --initiate or -i        : Generates a new controller handler. You should specify a controller name and the name should not be a number.'
    print '\t\t\t   The pattern is python box.py -i [controller name]'
    print ' --create or -c          : Create the database for the first usage. Only use this if you want to create the database for the first time'
    print ' --migrate or -m         : Create the migration script for migration process'
    print ' --upgrade or -u         : Upgrade the database to the latest migration version'
    print ' --downgrade or -d       : Downgrade the database to the previous migration version.'
    print '\t\t\t   To downgrade to a specific version use python box.py -d [version number]'
    print '--version or -v\t\t : Check current database version.'
    print ' --new or -n             : Create new data model.'
    print '\t\t\t   The pattern is box.py -n [model name] [<field name>:<field type>--<field length (if applicable. otherwise, default will be used)>]'
    print '\t\t\t   For more documentation please see http://docs.sqlalchemy.org/en/rel_0_7/core/types.html#types-generic'
    print ' --add or -a             : Install a new python package.'
    print '\t\t\t   The pattern is python box.py -a [package name]'
    print ' --help or -h            : Display the help file'
    print ''


def db_create():
    # This creates the new database.
    db.create_all()
    # If no repo existed, the creation will prepare for the first migration.
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        print '\nDatabase creation completed\n'
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))


def db_migrate():
    # This is used for database migration. Newly created database should go through this as well.
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
    # This is used for database migration upgrade.
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

    print 'Database upgrade completed!'
    print 'Current database version is: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))


def db_downgrade(version=None):
    # This is used to downgrade the database schema to a certain version or to one version before.
    # If you know exactly the version you wish to use then you can directly downgrade to that version.
    if not version:
        current_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        downgrade_version = current_version - 1
    else:
        downgrade_version = version
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, downgrade_version)

    print 'Database downgrade completed!'
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))


def add_model(model_name, model_components):
    # This is used to add model to the model file.

    # Get the current model file and open it for writing.
    model_path = os.path.join(BASEDIR, 'app/models.py')
    model_file = open(model_path, 'a')

    # Write the class definition.
    model_file.write('\n')
    model_file.write('class ' + model_name + '(db.Model):\n')
    model_file.write('\t' + model_name.lower() + '_id = db.Column(db.String(50), primary_key=True)\n')

    ## Add the model fields.
    ### First check for the data types and standardize it.
    for component in model_components:
        in_type = component['field_property'][0].lower()
        ### The database field type based on http://docs.sqlalchemy.org/en/rel_0_7/core/types.html#types-generic.
        if in_type == 'biginteger' or in_type == 'bigint' or in_type=='int' or in_type=='integer':
            data_type = 'Integer'
        elif in_type == 'boolean':
            data_type = 'Boolean'
        elif in_type == 'date':
            data_type = 'Date'
        elif in_type == 'datetime':
            data_type = 'DateTime'
        elif in_type == 'enum':
            data_type = 'Enum'
        elif in_type == 'float':
            data_type = 'Float'
        elif in_type == 'interval':
            data_type = 'Interval'
        elif in_type == 'largebinary':
            data_type = 'LargeBinary'
        elif in_type == 'numeric':
            data_type = 'Numeric'
        elif in_type == 'pickletype':
            data_type = 'PickleType'
        elif in_type == 'schematype':
            data_type = 'SchemaType'
        elif in_type == 'smallinteger' or in_type == 'smallint':
            data_type = 'SmallInteger'
        elif in_type == 'string':
            data_type = 'String'
        elif in_type == 'text':
            data_type = 'Text'
        elif in_type == 'time':
            data_type = 'Time'
        elif in_type == 'unicode':
            data_type = 'Unicode'
        elif in_type == 'unicodetext':
            data_type = 'UnicodeText'
        elif in_type == 'binary':
            data_type = 'Binary'
        elif in_type == 'blob':
            data_type = 'BLOB'
        else:

    ### If the data type did not match any of the existing data types, display error message and quit the program.
            print 'Data type ' + component['field_property'][0] + ' not found. Please refer to SQLAlchemy documentation for valid data types.'
            sys.exit()

    ### If it matches write the model fields into the model files.
        if len(component['field_property']) == 2:
            model_file.write('\t' + component['field_name'].lower() + ' = db.Column(db.' + data_type + '(' + component['field_property'][1] + '))\n')
        else:
            model_file.write('\t' + component['field_name'].lower() + ' = db.Column(db.' + data_type + ')\n')

    ## Create the class method for data transfer object (dto) for JSON representation.
    model_file.write('\n')
    model_file.write('\t# data transfer object to form JSON\n')
    model_file.write('\tdef dto(self):\n')
    model_file.write('\t\treturn dict(\n')

    ### Add the json component for all fields.
    mod_counter = 1
    model_file.write('\t\t\t\t' + model_name.lower() + '_id = self.' + model_name.lower() + '_id,\n')
    max_mod_index = len(model_components)

    for component in model_components:

        if mod_counter != max_mod_index:
            model_file.write('\t\t\t\t' + component['field_name'].lower() + ' = self.' + component['field_name'].lower() + ',\n')
        else:
            model_file.write('\t\t\t\t' + component['field_name'].lower() + ' = self.' + component['field_name'].lower() + ')\n')
        mod_counter = mod_counter + 1

    model_file.close()

    print '\n...........\n'

    # Add the JSON controller and CRUD controllers.
    add_model_json_controller_route(model_name)
    add_model_view_controller_and_template(model_name, model_components)
    add_single_views_controller_template(model_name,model_components)
    add_model_add_controller_template(model_name, model_components)
    add_model_create_controller(model_name, model_components)
    add_model_edit_controller_template(model_name, model_components)
    add_model_delete_controller(model_name, model_components)

    # perform the database creation and migration.
    # this will be based on the state of the database.
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        db_create()
        db_migrate()

    print "Please run box.py -m to complete the migration process"


def add_model_json_controller_route(model_name):
    # This is used to generate json callback handler for a specific model in the controller file.

    print "Generating model controller for JSON data access"

    model_controller_name = model_name.lower()
    db_model_name = model_name.title()

    # Get the controller file.
    controller_path = os.path.join(BASEDIR, 'app/main.py')

    # Read the original file.
    read_controller_file = open(controller_path, 'r')
    original_lines = read_controller_file.readlines()

    ## Add the model import to the controller import area.
    if original_lines[2] == 'import models\n':
        original_lines[2] = 'from models import ' + db_model_name + '\n'
    else:
        original_lines[2] = original_lines[2].strip()
        original_lines[2] = original_lines[2] + ', ' + db_model_name + '\n'
    controller_file = open(controller_path, 'w')

    for lines in original_lines:
        controller_file.write(lines)

    ## Write the handler definition.
    controller_file.write('\n\n')
    controller_file.write("########### " + model_name.lower() + " data model controllers area ###########\n\n")
    controller_file.write("@app.route('/data/" + model_name.lower() + "/')\n")
    controller_file.write("def data_" + model_controller_name + "():\n")

    ## Add the model fetch and JSON generation.
    controller_file.write("\t# this is the controller for JSON data access\n")
    controller_file.write("\t" + model_controller_name + "_list = " + model_name.title() + ".query.all()\n\n")
    controller_file.write("\tif " + model_controller_name + "_list:\n")
    controller_file.write("\t\tjson_result = json.dumps([" + model_controller_name + ".dto() for " + model_controller_name + " in " + model_controller_name + "_list])\n")
    controller_file.write("\telse:\n")
    controller_file.write("\t\tjson_result = None\n")

    ## Return the result
    controller_file.write("\n\treturn json_result\n\n")
    controller_file.close()

    print 'JSON data controller added'


def add_model_view_controller_and_template(model_name, model_components):
    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/main.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '.html')
    controller_file = open(controller_path, 'a')

    controller_file.write("@app.route('/" + model_name + "/')\n")
    controller_file.write("def " + model_name + "_view_controller():\n")
    controller_file.write("\t#this is the controller to view all data in the model\n")
    controller_file.write("\t" + model_name + "_list = " + model_name.title() + ".query.all()\n\n")
    controller_file.write("\tif " + model_name + "_list:\n")
    controller_file.write("\t\t" + model_name + "_entries = [" + model_name + ".dto() for " + model_name + " in " + model_name + "_list]\n")
    controller_file.write("\telse:\n")
    controller_file.write("\t\t" + model_name + "_entries = None\n\n")
    controller_file.write("\treturn render_template('" + model_name + ".html'," + model_name + "_entries = " + model_name + "_entries, title = \"" + model_name.title() + " List\")\n\n")

    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>List of " + model_name.title() + " Entries.</h1>\n")
    template_file.write("\t\t<table id=\"list-view\">\n")
    template_file.write("\t\t\t<thead>\n")
    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><b>ID</td>\n")

    for component in model_components:
        template_file.write("\t\t\t\t\t<td><b>" + component['field_name'].title() + "</b></td>\n")

    template_file.write("\t\t\t\t\t<td><b> </td>\n")
    template_file.write("\t\t\t\t\t<td><b> </td>\n")
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t\t</thead>\n")
    template_file.write("\t\t\t{% if " + model_name + "_entries %}\n")
    template_file.write("\t\t\t<tbody>\n")
    template_file.write("\t\t\t{% for entry in " + model_name + "_entries %}\n")
    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td>{{ entry.id }}</td>\n")

    for component in model_components:
        template_file.write("\t\t\t\t\t<td>{{ entry." + component['field_name'] + " }}</td>\n")

    template_file.write('\t\t\t\t\t<td><a href="/' + model_name + '/edit/{{ entry.' + model_name + '_id }}">Edit</a></td>\n')
    template_file.write('\t\t\t\t\t<td><a href="/' + model_name + '/delete/{{ entry.' + model_name + '_id }}">Delete</a></td>\n')
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t\t{% endfor %}\n")
    template_file.write("\t\t\t</tbody>\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\t\t{% else %}\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\tYou have no entries yet\n")
    template_file.write("\t\t\t{% endif %}\n")
    template_file.write('\t\t\t<br/><br/><b><a id="actions" href="/' + model_name + '/add">Add new entry</a></b>\n')
    template_file.write("{% endblock %}\n")

    print 'Entries view controller added'

def add_single_views_controller_template(model_name, model_components):
    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/main.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_view.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("def get_single_"+model_name+"("+model_name+"_id):\n")
    controller_file.write("\t"+model_name+" = None\n")
    controller_file.write("\tsingle_"+model_name+" = "+model_name.title()+".query.filter("+model_name.title()+"."+model_name+"_id == "+model_name+"_id).first()\n")
    controller_file.write("\tif single_"+model_name+":\n")
    controller_file.write("\t\t"+model_name+" = single_"+model_name+".dto()\n")
    controller_file.write("\tresult = "+model_name+"\n")
    controller_file.write("\treturn result\n\n")

    controller_file.write("@app.route('/" + model_name + "/<"+model_name+"_id>.json')\n")
    controller_file.write("def get_single_" + model_name + "_json("+model_name+"_id):\n")
    controller_file.write("\t#this is the controller to get single entry in json format\n")
    controller_file.write("\tresult = json.dumps(dict("+model_name+"=get_single_"+model_name+"("+model_name+"_id)))\n")
    controller_file.write("\treturn result\n\n")

    controller_file.write("@app.route('/" + model_name + "/<"+model_name+"_id>')\n")
    controller_file.write("def view_single_" + model_name + "("+model_name+"_id):\n")
    controller_file.write("\t#this is the controller to get single entry view\n")
    controller_file.write("\t"+model_name+" = get_single_"+model_name+"("+model_name+"_id)\n")
    controller_file.write("\treturn render_template('"+model_name+"_view.html', "+model_name+" = "+model_name+")\n\n")

    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>View " + model_name.title() + " single entry.</h1>\n")
    template_file.write("\t\t<table>\n")

    for component in model_components:
        template_file.write("\t\t\t\t<tr>\n")
        template_file.write("\t\t\t\t\t<td>" + component['field_name'].title() + ":</td>\n")
        template_file.write("\t\t\t\t\t<td>{{ " + model_name + "_item." + component['field_name'].lower() + " }}</td>\n")
        template_file.write("\t\t\t\t</tr>\n")

    template_file.write("\t\t</table>\n")
    template_file.write("{% endblock %}")

    print 'Single entries view and controller added'


def add_model_add_controller_template(model_name, model_components):

    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/main.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_add.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("@app.route('/" + model_name + "/add/')\n")
    controller_file.write("def " + model_name + "_add_controller():\n")
    controller_file.write("\t#this is the controller to add new model entries\n")
    controller_file.write("\treturn render_template('" + model_name + "_add.html', title = \"Add New Entry\")\n\n")

    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>Add new " + model_name.title() + " Entries.</h1>\n")
    template_file.write("\t\t<form name=\"" + model_name + "_add\" method=\"post\" action=\"/" + model_name + "/create/\">\n")
    template_file.write("\t\t<table>\n")

    for component in model_components:
        template_file.write("\t\t\t\t<tr>\n")
        template_file.write("\t\t\t\t\t<td>" + component['field_name'].title() + ":</td>\n")
        template_file.write("\t\t\t\t\t<td><input type=\"text\" name=\"" + component['field_name'].lower() + "\"/></td>\n")
        template_file.write("\t\t\t\t</tr>\n")

    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><input type=\"submit\" name=\"submit\" value=\"Add Entry\"/></td>\n")
    template_file.write("\t\t\t\t\t<td> </td>\n")
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\t</form>\n")
    template_file.write("{% endblock %}")

    print 'Entries add form controller added'


def add_model_edit_controller_template(model_name, model_components):
    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/main.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_edit.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("@app.route('/" + model_name + "/edit/<id>')\n")
    controller_file.write("def " + model_name + "_edit_controller(id):\n")
    controller_file.write("\t#this is the controller to edit model entries\n")
    controller_file.write("\t" + model_name + "_item = " + model_name.title() + ".query.filter(" + model_name.title() + "." + model_name + "_id == id).first()\n")
    controller_file.write("\treturn render_template('" + model_name + "_edit.html', " + model_name + "_item = " + model_name + "_item, title = \"Edit Entries\")\n\n")

    template_file = open(template_path, 'w')
    template_file.write("{% extends \"base.html\" %}\n")
    template_file.write("{% block content %}\n")
    template_file.write("\t\t<h1>Edit " + model_name.title() + " Entries.</h1>\n")
    template_file.write("\t\t<form name=\"" + model_name + "_add\" method=\"post\" action=\"/" + model_name + "/update/{{ " + model_name + "_item." + model_name + "_id }}\">\n")
    template_file.write("\t\t<table>\n")

    for component in model_components:
        template_file.write("\t\t\t\t<tr>\n")
        template_file.write("\t\t\t\t\t<td>" + component['field_name'].title() + ":</td>\n")
        template_file.write("\t\t\t\t\t<td><input type=\"text\" name=\"" + component['field_name'].lower() + "\" value=\"{{ " + model_name + "_item." + component['field_name'].lower() + " }}\"/></td>\n")
        template_file.write("\t\t\t\t</tr>\n")

    template_file.write("\t\t\t\t<tr>\n")
    template_file.write("\t\t\t\t\t<td><input type=\"submit\" name=\"submit\" value=\"Edit Entry\"/></td>\n")
    template_file.write("\t\t\t\t\t<td> </td>\n")
    template_file.write("\t\t\t\t</tr>\n")
    template_file.write("\t\t</table>\n")
    template_file.write("\t\t</form>\n")
    template_file.write("{% endblock %}")
    controller_file = open(controller_path, 'a')
    controller_file.write("@app.route('/" + model_name + "/update/<id>',methods=['POST','GET'])\n")
    controller_file.write("def " + model_name + "_update_data_controller(id):\n")
    controller_file.write("\t# this is the " + model_name + " data update handler\n")

    for component in model_components:
        controller_file.write("\t" + component['field_name'].lower() + " = request.values.get('" + component['field_name'].lower() + "')\n")

    controller_file.write("\t" + model_name + "_item = " + model_name.title() + ".query.filter(" + model_name.title() + "." + model_name + "_id == id).first()\n")

    for component in model_components:
        controller_file.write("\t" + model_name + "_item." + component['field_name'].lower() + " = " + component['field_name'].lower() + "\n")

    controller_file.write("\n\tdb.session.add(" + model_name + "_item)\n")
    controller_file.write("\tdb.session.commit()\n")
    controller_file.write("\n\treturn 'data update successful <a href=\"/" + model_name + "/\">back to Entries</a>'\n\n")

    print 'Entries edit and update form controller added'


def add_model_create_controller(model_name, model_components):
    model_name = model_name.lower()
    mod_counter = 1
    max_mod_index = len(model_components)
    controller_path = os.path.join(BASEDIR, 'app/main.py')

    controller_file = open(controller_path, 'a')
    controller_file.write("@app.route('/" + model_name + "/create/',methods=['POST','GET'])\n")
    controller_file.write("def " + model_name + "_create_data_controller():\n")
    controller_file.write("\t# this is the " + model_name + " data create handler\n")

    for component in model_components:
        controller_file.write("\t" + component['field_name'].lower() + " = request.values.get('" + component['field_name'].lower() + "')\n")

    controller_file.write("\n\tnew_" + model_name + " = " + model_name.title() + "(\n")
    controller_file.write("\t\t\t\t\t\t\t\t\t" + model_name + '_id = generate_key(),\n')

    for component in model_components:
        if mod_counter != max_mod_index:
            controller_file.write("\t\t\t\t\t\t\t\t\t" + component['field_name'].lower() + ' = ' + component['field_name'].lower() + ',\n')
        else:
            controller_file.write("\t\t\t\t\t\t\t\t\t" + component['field_name'].lower() + ' = ' + component['field_name'].lower() + '\n')
        mod_counter = mod_counter + 1

    controller_file.write("\t\t\t\t\t\t\t\t)\n")
    controller_file.write("\n\tdb.session.add(new_" + model_name + ")\n")
    controller_file.write("\tdb.session.commit()\n")
    controller_file.write("\n\treturn 'data input successful <a href=\"/" + model_name + "/\">back to Entries</a>'\n\n")

    print 'Entries creation controller added'


def add_model_delete_controller(model_name, model_components):
    model_name = model_name.lower()
    controller_path = os.path.join(BASEDIR, 'app/main.py')
    template_path = os.path.join(BASEDIR, 'app/templates/' + model_name + '_add.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("@app.route('/" + model_name + "/delete/<id>')\n")
    controller_file.write("def " + model_name + "_delete_controller(id):\n")
    controller_file.write("\t#this is the controller to delete model entries\n")
    controller_file.write("\t" + model_name + "_item = " + model_name.title() + ".query.filter(" + model_name.title() + "." + model_name + "_id == id).first()\n")
    controller_file.write("\n\tdb.session.delete(" + model_name + "_item)\n")
    controller_file.write("\tdb.session.commit()\n")
    controller_file.write("\n\treturn 'data deletion successful <a href=\"/" + model_name + "/\">back to Entries</a>'\n\n")

    print 'Entries deletion controller added'


def add_controller(controller_name):
    controller_name = controller_name.lower()
    controller_name = controller_name.replace(' ', '_')
    controller_name = controller_name.replace('\'', '_')
    controller_name = controller_name.replace('.', '_')
    controller_name = controller_name.replace(',', '_')
    controller_path = os.path.join(BASEDIR, 'app/main.py')
    view_path = os.path.join(BASEDIR, 'app/templates/' + controller_name + '.html')

    controller_file = open(controller_path, 'a')
    controller_file.write("\n\n@app.route('/" + controller_name + "/') #Link\n")
    controller_file.write("def " + controller_name + "_control():\n")
    controller_file.write("\t# add your controller here\n")
    controller_file.write("\treturn render_template('" + controller_name + ".html')\n")
    controller_file.close()

    print '\nController generated\n'

    view_file = open(view_path, 'a')
    view_file.write("{% extends \"base.html\" %}\n")
    view_file.write("{% block content %}\n")
    view_file.write('\t\t<h1>The ' + controller_name.lower() + ' view.</h1>\n')
    view_file.write('\t\t<p>You can change this view in ' + view_path + '</p>\n')
    view_file.write("{% endblock %}")

    print '\nview file generated and available at ' + view_path + '\n'


def db_version():
    # this is used to get the latest version in the database
    current_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

    print 'The current database version is ' + str(current_version)


def install_package(package_name):
    if not package_name:
        print "You need to specify a valid package name"
    else:
        current_platform = platform.system()
        bin_base = ''
        if current_platform == 'Windows':
            bin_base = 'box\Scripts\pip'
        else:
            bin_base = 'box/bin/pip'

        call([bin_base, 'install', package_name.lower()])


if len(sys.argv) > 1:
    sysinput = sys.argv[1].lower()

    if sysinput == '--help' or sysinput == '-h':
        help()

    elif sysinput == '--add' or sysinput == '-a':
        if sys.argv[2]:
            install_package(sys.argv[2])
        else:
            print "You need to specify a valid package name"
            sys.exit()

    elif sysinput == '--create' or sysinput == '-c':
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            db_create()
        else:
            print '\nPrevious database version found. Please use -m or --migrate option\n'
            sys.exit()

    elif sysinput == '--migrate' or sysinput == '-m':
        db_migrate()

    elif sysinput == '--initiate' or sysinput == '-i':
        if len(sys.argv) > 2 and not sys.argv[2].isdigit():
            add_controller(sys.argv[2])
        else:
            print 'Controller name can not be a number'
            sys.exit()

    elif sysinput == '--upgrade' or sysinput == '-u':
        db_upgrade()

    elif sysinput == '--version' or sysinput == '-v':
        db_version()

    elif sysinput == '--downgrade' or sysinput == '-d':
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            db_downgrade(sys.argv[2])
        else:
            db_downgrade()

    elif sysinput == '--new' or sysinput == '-n':
        if len(sys.argv) > 2:
            model_name = sys.argv[2].title()
            raw_component = sys.argv[3:]
            if raw_component:
                model_components = []

                for component in raw_component:
                    raw_field = component.split(':')
                    field_name = raw_field[0]
                    detail_components = raw_field[1].split('--')
                    if detail_components[0].lower() == 'string':
                        if len(detail_components) < 2:
                            detail_components.append('50')
                    insert_components = {
                        'field_name': field_name,
                        'field_property': detail_components
                    }
                    model_components.append(insert_components)
            else:
                print '\nNot enough parameters are provided. Model requires field definitions. See box.py -h for info\n'
                sys.exit()
            add_model(model_name, model_components)
        else:
            print '\nNot enough parameters are provided. See box.py -h for info\n'

    else:
        print '\nCommand not found. Please use --help for command options\n'

else:
    print '\nNot enough parameters found. Please run box.py -h for complete explanations\n'


# end of file