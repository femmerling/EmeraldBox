import platform
import re

from subprocess import call, Popen, PIPE

from config import SERVER_PORT

current_platform = platform.system()
bin_base = 'box/bin/python'
if current_platform == 'Windows':
    bin_base = 'box\Scripts\python'

def run_tornado():
    call([bin_base,'ignite.py'])

def run_testrun():
    call([bin_base,'testrun.py'])

def run_gunicorn(arguments = None):
    option_list = [bin_base,'-b','0.0.0.0:'+str(SERVER_PORT),'greeny:app']
    try:
        restart_gunicorn()
        if arguments:
            for item in arguments:
                option_list.append(item)
            call(option_list)
        else:
            call([bin_base,'-b','0.0.0.0:'+str(SERVER_PORT),'-w','4','-k','tornado','greeny:app','--daemon'])
    except:
        if arguments:
            for item in arguments:
                option_list.append(item)
            call(option_list)
        else:
            call([bin_base,'-b','0.0.0.0:'+str(SERVER_PORT),'-w','4','-k','tornado','greeny:app','--daemon'])

def restart_gunicorn():
    proc = Popen(['ps','aux'], stdout=PIPE)
    output=proc.communicate()[0].split('\n')
    processes = output[2:]
    ids = []
    for item in processes:
        if re.search('gunicorn',item):
            values=[]
            strings = item.split(" ")
            for x in strings:
                if x != "":
                    values.append(x)
            ids.append(values[1])

    ids.sort()
    call(['kill','-9',ids[0]])


# end of file