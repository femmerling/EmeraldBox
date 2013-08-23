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
    print ' --serve or -s            : Run The Tornado Web Server'
    print ' --gserve or -g            : Run The Gunicorn Web Server. You can add your own gunicorn options aside from bind address and port'
    print ' --testrun or -t            : Run The Development Server'
    print ''


# end of file