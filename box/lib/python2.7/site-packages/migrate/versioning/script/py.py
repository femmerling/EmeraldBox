from script import *
from logsql import LogsqlFile
from migrate.versioning.template import template
from migrate.versioning import exceptions
import sqlalchemy
import migrate.run

class PythonFile(ScriptFile):
    def __init__(self,path):
        super(PythonFile,self).__init__(path)
        #self.module=import_path(path)

    def _get_module(self):
        if not hasattr(self,'_module'):
            self._module = self.verify_module(self.path)
        return self._module
    module = property(_get_module)

    def _get_logsql(self):
        try:
            return self.module.logsql
        except AttributeError:
            return False
    logsql = property(_get_logsql)

    @classmethod
    def create(cls,path,**opts):
        """Create an empty migration script"""
        cls.require_notfound(path)

        filename = None
        if opts.get('logsql',False):
            filename = 'logsql.py_tmpl'
        src=template.get_script(filename)
        shutil.copy(src,path)

    @classmethod
    def verify(cls,path):
        # Verifying valid python script is done when .module is referenced
        super(PythonFile,cls).verify(path)

    @classmethod
    @logsql_engine
    def verify_module(cls,path):
        """Ensure this is a valid script, or raise InvalidScriptError"""
        # Try to import and get the upgrade() func
        try:
            module=import_path(path)
        except:
            # If the script itself has errors, that's not our problem
            raise
        try:
            assert callable(module.upgrade)
        except Exception,e:
            raise exceptions.InvalidScriptError(path+': %s'%str(e))
        return module

    def _func(self,funcname):
        try:
            return getattr(self.module,funcname)
        except AttributeError:
            msg = "The function %s is not defined in this script"
            raise exceptions.ScriptError(msg%funcname)
            

    @logsql_engine
    def compile(self,database,operation,path=None):
        """Compile a Python script into a logfile or log object"""
        # Change the engine referenced by all migration scripts
        try:
            self.module.migrate_engine.reset(database)
            #migrate.run.migrate_engine.reset(database)
        except (ImportError,sqlalchemy.exceptions.InvalidRequestError,
                AttributeError,#sqlite
                ):
            raise exceptions.ScriptError("The database %s doesn't exist"%database)
        # Run the migration function. Must exist if script/op are valid
        try:
            funcname = operations[operation]
        except KeyError:
            raise exceptions.ScriptError("%s is not a valid migration function"%operation)
        func = self._func(funcname)
        func()
        # Success - return the log, or a file containing the log if path given
        ret = self.module.migrate_engine.logsql
        #ret = migrate.run.migrate_engine.logsql
        if path is not None:
            ret = LogsqlFile.create(ret,path)
        return ret
    
    def run(self,engine,step):
        if step > 0:
            op = 'upgrade'
        elif step < 0:
            op = 'downgrade'
        else:
            raise exceptions.ScriptError("%d is not a valid step"%step)
        funcname = operations[op]

        migrate.run.migrate_engine = engine
        #self.module.migrate_engine = engine
        func = self._func(funcname)
        func()
        migrate.run.migrate_engine = None
