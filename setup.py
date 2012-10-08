from subprocess import call
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))
virtualenv_path = os.path.join(basedir, 'virtualenv.py')
python_path = os.path.join(basedir, 'flask/bin/python')
pip_path = os.path.join(basedir, 'flask/bin/pip')
call(['python', virtualenv_path, 'flask'])
print '\nYour EmeraldBox instalation is ready to use.'
print '\nRun box.py -h for full details on how to use the box tools or run ignite.py to run the server.\n'