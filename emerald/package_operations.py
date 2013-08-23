import platform

from subprocess import call

def install_package(package_name):
    if not package_name:
        print "You need to specify a valid package name"
    else:
        current_platform = platform.system()
        bin_base = ''
        if current_platform == 'Windows':
            bin_base = 'box\Scripts\pip'
        else:
            bin_base = 'box/bin/pip'

        call([bin_base, 'install', package_name.lower()])


# end of file