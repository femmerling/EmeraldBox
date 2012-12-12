from subprocess import call
from config import BASEDIR, ADDITIONAL_PACKAGES
import os.path
import platform

current_platform = platform.system()
virtualenv_path = os.path.join(BASEDIR, 'virtualenv.py')
box_path = os.path.join(BASEDIR, 'box.py')
ignite_path = os.path.join(BASEDIR, 'ignite.py')

def update_environment(file_path):
	update_file = open(file_path, 'r')
	original_lines = update_file.readlines()
	if current_platform == 'Windows':
		original_lines[0] = '#! box\Scripts\python\n'
	else:
		original_lines[0] = '#! box/bin/python\n'
	update_file.close()
	update_file = open(file_path, 'w')
	for lines in original_lines:
		update_file.write(lines)

	update_file.close()

update_environment(box_path)
update_environment(ignite_path)

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

print 'installing Tornado Web Server\n'
call([bin_base, 'install', 'tornado'])
print '\nTornado Web Server installed\n'
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