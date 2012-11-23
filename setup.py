from subprocess import call
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))
virtualenv_path = os.path.join(basedir, 'virtualenv.py')
box_path = os.path.join(basedir, 'box.py')
ignite_path = os.path.join(basedir, 'ignite.py')
db_path = os.path.join(basedir, 'db/')
call(['mkdir',db_path])
call(['python', virtualenv_path, 'box'])
call(['chmod','a+x', box_path])
call(['chmod','a+x', ignite_path])
print 'new environment created, now installing components\n'
print 'installing Flask\n'
call(['box/bin/pip','install','flask'])
print 'Flask installed\n'
print 'installing Flask-Mail\n'
call(['box/bin/pip','install','Flask-Mail'])
print 'Flask-Mail installed\n'
print 'installing SQLAlchemy\n'
call(['box/bin/pip','install','sqlalchemy'])
print 'SQLAlchemy installed\n'
print 'installing Flask-SQLAlchemy\n'
call(['box/bin/pip','install','flask-sqlalchemy'])
print 'Flask-SQLAlchemy installed\n'
print 'installing SQLAlchemy-Migrate\n'
call(['box/bin/pip','install','sqlalchemy-migrate'])
print 'SQLAlchemy-Migrate installed\n'
print '##################################################'
print '# IMPORTANT                                      #'
print	'# to use SQLAlchemy with MySQL, PostgreSQL and   #'
print '# Oracle, you need to install additional modules #'
print '##################################################\n'
print 'installing Tornado Web Server\n'
call(['box/bin/pip','install','tornado'])
print 'Tornado Web Server installed\n'
print 'installing Nosetest\n'
call(['box/bin/pip','install','nose'])
print 'Nosetest installed\n'
print '\nAll basic packages have been installed!\n'
print '\nYour basic EmeraldBox instalation is ready to use.'
print '\nRun ./box.py -h for full details on how to use the box tools or run ./ignite.py to run the server.\n'
print '\nEnjoy your time with EmeraldBox and thank your for using!\n\n'