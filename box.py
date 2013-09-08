#! box/bin/python

"""
box.py

author: erich@emfeld.com
========================

This file is the main file that binds all the functions in the
emerald directory.

The file handles all generator and database operations from the command line.

Running the server is performed by this file.

The file depends on the emerald module.

"""
import sys
import os.path

from config import SQLALCHEMY_MIGRATE_REPO, VALID_DATA_TYPES

from emerald import help, db_create, db_migrate 
from emerald import db_upgrade, db_downgrade, db_version
from emerald import install_package
from emerald import add_controller, add_model
from emerald import run_tornado, run_gunicorn, run_testrun

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

    elif sysinput == '--serve' or sysinput == '-s':
        run_tornado()

    elif sysinput == '--gserve' or sysinput == '-g':
        if len(sys.argv) > 2:
            run_gunicorn(sys.argv[2:])
        else:
            run_gunicorn()
        

    elif sysinput == '--testrun' or sysinput == '-t':
        run_testrun()


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
            if raw_component:
                for component in raw_component:
                    raw_field = component.split(':')
                    field_name = raw_field[0]
                    detail_components = raw_field[1].split('--')
                    if detail_components[0].lower() == 'string':
                        if len(detail_components) <= 2:
                            detail_components.append('50')
                            insert_components = {
                                'field_name': field_name,
                                'field_property': detail_components
                            }
                    elif detail_components[0].lower() in VALID_DATA_TYPES:
                        insert_components = {
                            'field_name': field_name,
                            'field_property': detail_components
                        }
                    else:
                        print '\n' + detail_components[0].lower() + ' is not a valid data type.'
                        sys.exit()
                    model_components.append(insert_components)
                add_model(model_name, model_components)
            else:
                print '\nNot enough parameters are provided. Model requires field definitions. See box.py -h for info\n'
                sys.exit()
        else:
            print '\nNot enough parameters are provided. See box.py -h for info\n'

    else:
        print '\nCommand not found. Please use --help for command options\n'

else:
    print '\nNot enough parameters found. Please run box.py -h for complete explanations\n'


# end of file