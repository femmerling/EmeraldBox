from migrate.versioning.base import *
from migrate.versioning.pathed import * 
from migrate.versioning import exceptions
import os
import sys
import sqlalchemy
import migrate.run

def import_path(fullpath):
    """ Import a file with full path specification. Allows one to
        import from anywhere, something __import__ does not do. 
    """
     # http://zephyrfalcon.org/weblog/arch_d7_2002_08_31.html
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date during tests
    del sys.path[-1]
    return module

def logsql_engine(func,force=False):
    """migrate.run.migrate_engine is a logengine in the decorated function"""
    def entangle(*p,**k):
        if force or (not getattr(migrate.run,'migrate_engine',None)):
            migrate.run.migrate_engine = sqlalchemy.create_engine(None,strategy='logsql')
        reload(migrate)
        try:
            return func(*p,**k)
        finally:
            try:
                del migrate.run.migrate_engine
            except AttributeError:
                # If this disappeared on its own, that's ok
                pass
    return entangle

class ScriptFile(Pathed):
    """Base class for other types of scripts
    All scripts have the following properties:

    source (script.source())
      The source code of the script
    version (script.version())
      The version number of the script
    operations (script.operations())
      The operations defined by the script: upgrade(), downgrade() or both.
      Returns a tuple of operations.
      Can also check for an operation with ex. script.operation(Script.ops.up)
    """
    logsql = None
    """If true, this file should be compiled upon commit"""

    def __init__(self,path):
        log.info('Loading script %s...'%path)
        self.verify(path)
        super(ScriptFile,self).__init__(path)
        log.info('Script %s loaded successfully'%path)
    
    @classmethod
    def verify(cls,path):
        """Ensure this is a valid script, or raise InvalidScriptError
        Child classes might add to this by extending _verify
        """
        try:
            cls.require_found(path)
        except:
            raise exceptions.InvalidScriptError(path)

    def version(self):
        raise NotImplementedError()   #TODO
    def source(self):
        fd=open(self.path)
        ret=fd.read()
        fd.close()
        return ret
    def operations(self):
        # Must be defined in child class
        raise NotImplementedError()
    def operation(self,op):
        return op in self.operations()

    def run(self,engine):
        raise NotImplementedError()
