"""
setup.py

author: erich@emfeld.com
========================

This file will create the environment in which the EmeraldBox app lives in

To use the file simply run python setup.py

The file will install basic packages of EmeraldBox, which are:
- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- SQLAlchemy-Migrate
- Tornado
- Gunicorn

Additional packages that you may require can be defined in config.py file
using the list of ADDITIONAL_PACKAGES

Note:
Please remember to add mysql-python to ADDITIONAL_PACKAGES if you wish to
use MySQL as your database

"""


import os.path
import platform

from subprocess import call

from config import BASEDIR, ADDITIONAL_PACKAGES

current_platform = platform.system()

#this is the path to the virtualenv file
virtualenv_path = os.path.join(BASEDIR, 'virtualenv.py')

#this is the path to the box.py file
box_path = os.path.join(BASEDIR, 'box.py')

#this is the path to the ignite.py file
ignite_path = os.path.join(BASEDIR, 'ignite.py')

#this is the path to the testrun.py file
testrun_path = os.path.join(BASEDIR, 'testrun.py')

#this is the path to the greeny.py file
green_path = os.path.join(BASEDIR, 'greeny.py')


"""
This will auto adjust the python runtime being used by the file.

Todo:
On windows this has no effect. Need to do more research on making 
it executable like in UNIX/Linux

"""

def update_environment(file_path):
	update_file = open(file_path, 'r')
	original_lines = update_file.readlines()
	original_lines[0] = '#! box/bin/python\n'
	if current_platform == 'Windows':
		original_lines[0] = '#! box\Scripts\python\n'
	update_file.close()
	update_file = open(file_path, 'w')
	for lines in original_lines:
		update_file.write(lines)

	update_file.close()


"""
This is to fix the migrate versioning bug.
Will be removed when the bug on the original package is fixed

"""

def tempfix_migrate():
	print "\nFixing the migrate bug \n"
	buggy_path = os.path.join(BASEDIR, 
					 'box/lib/python2.7/site-packages/migrate/versioning/schema.py')
	if current_platform == 'Windows':
		buggy_path = os.path.join(BASEDIR, 
					 'box\lib\site-packages\migrate\\versioning\schema.py')
	buggy_file = open(buggy_path,'r')
	original_lines = buggy_file.readlines()
	original_lines[9] = "\n"
	buggy_file.close()
	update_file = open(buggy_path,'w')
	for lines in original_lines:
		update_file.write(lines)
	update_file.close()



update_environment(box_path)
update_environment(ignite_path)
update_environment(testrun_path)
update_environment(green_path)

bin_base = 'box/bin/pip'
if current_platform == 'Windows':
	bin_base = 'box\Scripts\pip'
	if not os.path.exists(os.path.join(BASEDIR, 'db\\')):
		os.makedirs(os.path.join(BASEDIR, 'db\\'))
	call(['python', virtualenv_path, 'box'])	
else:
	if not os.path.exists(os.path.join(BASEDIR, 'db/')):
		os.makedirs(os.path.join(BASEDIR, 'db/'))
	call(['python', virtualenv_path, 'box'])
	call(['chmod', 'a+x', box_path])
	call(['chmod', 'a+x', ignite_path])
	call(['chmod', 'a+x', testrun_path])


print 'new environment created, now installing components\n'

print 'installing Flask\n'
call([bin_base, 'install', 'flask'])
print '\nFlask installed\n'

print 'installing SQLAlchemy\n'
call([bin_base, 'install', 'sqlalchemy'])
print '\nSQLAlchemy installed\n'

print 'installing Flask-SQLAlchemy\n'
call([bin_base, 'install', 'flask-sqlalchemy'])
print '\nFlask-SQLAlchemy installed\n'

print 'installing SQLAlchemy-Migrate\n'
call([bin_base, 'install', 'sqlalchemy-migrate'])
print '\nSQLAlchemy-Migrate installed\n'
print '##################################################'
print '# IMPORTANT                                      #'
print '# to use SQLAlchemy with MySQL, PostgreSQL and   #'
print '# Oracle, you need to install additional modules #'
print '##################################################\n'

tempfix_migrate()

print 'installing Tornado Web Server\n'
call([bin_base, 'install', 'tornado'])
print '\nTornado Web Server installed\n'

print 'installing Gunicorn Web Server\n'
call([bin_base, 'install', 'gunicorn'])
print '\nGunicorn Web Server installed\n'

print '\nAll basic packages have been installed!\n'
print '\nYour basic EmeraldBox instalation is ready to use.\n'

if len(ADDITIONAL_PACKAGES) > 0:
	print '\nNow installing additional packages\n'
	for package in ADDITIONAL_PACKAGES:
		print 'installing ' + package.title() + "\n"
		call([bin_base,'install',package])
		print "\n" + package.title() + " installed\n"

	print '\nAll packages installed.\n'


print '\nRun ./box.py -h for full details on how to use the box tools or run ./ignite.py to run the server.\n'
print '\nEnjoy your time with EmeraldBox and thank your for using!\n\n'


# end of file