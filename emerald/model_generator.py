import os.path
import sys

from config import BASEDIR
from config import WHITE_SPACE
from config import SQLALCHEMY_MIGRATE_REPO

from database_operations import db_create, db_migrate
from controller_generator import generate_controller
from template_generator import generate_index_template
from template_generator import generate_controller_template
from template_generator import generate_edit_template
from template_generator import generate_view_template

def add_model(model_name, model_components):
    # This is used to add model to the model file.

    # Get the current model file and open it for writing.
    model_path = os.path.join(BASEDIR, "app/models/" + model_name.lower() + ".py")
    init_path = os.path.join(BASEDIR, "app/models/__init__.py")
    model_file = open(model_path, 'w')


    # Write the class definition.
    model_file.write('from app import db\n\n')
    model_file.write('class ' + model_name.title() + '(db.Model):\n')
    model_file.write(WHITE_SPACE+'id = db.Column(db.Integer, primary_key=True)\n')

    ## Add the model fields.
    ### First check for the data types and standardize it.
    for component in model_components:
        in_type = component['field_property'][0].lower()
        ### The database field type based on http://docs.sqlalchemy.org/en/rel_0_7/core/types.html#types-generic.
        if in_type == 'biginteger' or in_type == 'bigint':
            data_type = 'BigInteger'
        elif in_type=='int' or in_type=='integer':
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
            model_file.write(WHITE_SPACE + component['field_name'].lower() + ' = db.Column(db.' + data_type + '(' + component['field_property'][1] + '))\n')
        else:
            model_file.write(WHITE_SPACE + component['field_name'].lower() + ' = db.Column(db.' + data_type + ')\n')

    ## Create the class method for data transfer object (dto) for JSON representation.
    model_file.write('\n')
    model_file.write(WHITE_SPACE + '# data transfer object to form JSON\n')
    model_file.write(WHITE_SPACE + 'def dto(self):\n')
    model_file.write(WHITE_SPACE + WHITE_SPACE + 'return dict(\n')

    ### Add the json component for all fields.
    mod_counter = 1
    model_file.write(WHITE_SPACE+WHITE_SPACE+WHITE_SPACE+'id = self.id,\n')
    max_mod_index = len(model_components)

    for component in model_components:

        if mod_counter != max_mod_index:
            model_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + component['field_name'].lower() + ' = self.' + component['field_name'].lower() + ',\n')
        else:
            model_file.write(WHITE_SPACE + WHITE_SPACE + WHITE_SPACE + component['field_name'].lower() + ' = self.' + component['field_name'].lower() + ')\n')
        mod_counter = mod_counter + 1

    model_file.close()

    init_file = open(init_path, 'a')
    init_file.write("from "+ model_name.lower() + " import " + model_name.title()+"\n")
    init_file.close()

    print '\n...........\n'

    #add the CRUD controllers
    generate_controller(model_name, model_components)
    generate_index_template(model_name, model_components)
    generate_controller_template(model_name, model_components)
    generate_edit_template(model_name, model_components)
    generate_view_template(model_name, model_components)

    # perform the database creation and migration.
    # this will be based on the state of the database.
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        db_create()
        db_migrate()

    print "Please run box.py -m to complete the migration process"


# end of file