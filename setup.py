from subprocess import call
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))
virtualenv_path = os.path.join(basedir, 'virtualenv.py')
box_path = os.path.join(basedir, 'box.py')
ignite_path = os.path.join(basedir, 'ignite.py')
call(['python', virtualenv_path, 'flask'])
call(['chmod','a+x', box_path])
call(['chmod','a+x', ignite_path])
print '\nYour EmeraldBox instalation is ready to use.'
print '\nRun ./box.py -h for full details on how to use the box tools or run ./ignite.py to run the server.\n'