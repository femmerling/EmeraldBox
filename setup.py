from subprocess import call
import os.path
import platform

current_platform = platform.system()
basedir = os.path.abspath(os.path.dirname(__file__))
virtualenv_path = os.path.join(basedir, 'virtualenv.py')
box_path = os.path.join(basedir, 'box.py')
ignite_path = os.path.join(basedir, 'ignite.py')
db_path = os.path.join(basedir, 'db/')


def update_environment(file_path):
	update_file = open(file_path, 'r')
	original_lines = update_file.readlines()
	if current_platform == 'Windows':
		original_lines[0] = '#! box/Scripts/python\n'
	else:
		original_lines[0] = '#! box/bin/python\n'
	update_file.close()
	update_file = open(file_path, 'w')
	for lines in original_lines:
		update_file.write(lines)

	update_file.close()


bin_base = ''
if current_platform == 'Windows':
	bin_base = 'box\Scripts\pip'
else:
	bin_base = 'box/bin/pip'


update_environment(box_path)
update_environment(ignite_path)

call(['mkdir', db_path])

call(['python', virtualenv_path, 'box'])

call(['chmod', 'a+x', box_path])

call(['chmod', 'a+x', ignite_path])



print 'new environment created, now installing components\n'

print 'installing Flask\n'
call([bin_base, 'install', 'flask'])
print 'Flask installed\n'

print 'installing Flask-Mail\n'
call([bin_base, 'install', 'Flask-Mail'])
print 'Flask-Mail installed\n'

print 'installing SQLAlchemy\n'
call([bin_base, 'install', 'sqlalchemy'])
print 'SQLAlchemy installed\n'

print 'installing Flask-SQLAlchemy\n'
call([bin_base, 'install', 'flask-sqlalchemy'])
print 'Flask-SQLAlchemy installed\n'

print 'installing SQLAlchemy-Migrate\n'
call([bin_base, 'install', 'sqlalchemy-migrate'])
print 'SQLAlchemy-Migrate installed\n'
print '##################################################'
print '# IMPORTANT                                      #'
print	'# to use SQLAlchemy with MySQL, PostgreSQL and   #'
print '# Oracle, you need to install additional modules #'
print '##################################################\n'

print 'installing Tornado Web Server\n'
call([bin_base, 'install', 'tornado'])
print 'Tornado Web Server installed\n'

print 'installing Nosetest\n'
call([bin_base, 'install', 'nose'])
print 'Nosetest installed\n'

print '\nAll basic packages have been installed!\n'
print '\nYour basic EmeraldBox instalation is ready to use.'
print '\nRun ./box.py -h for full details on how to use the box tools or run ./ignite.py to run the server.\n'
print '\nEnjoy your time with EmeraldBox and thank your for using!\n\n'

