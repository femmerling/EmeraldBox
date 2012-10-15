"""SQL statements are logged to a file, which may be run later with consistent results.

This implies that this engine is write-only: SQL for all selects/reads will
be output to a log, but you cannot manipulate their results, as the statements 
are not actually executed.

Usage::

>>>from migrate.versioning import logengine
>>># Create an engine with the log strategy
>>>engine=create_engine('sqlite:///:memory:',strategy='logsql')
>>>
>>># Run some SQL to be logged. 
>>># This is write-only: you can't analyze the results!
>>>select(['42'],engine=engine).execute()
>>>
>>># Save the log to a file
>>>engine.write("filename.logsql")
>>># Or save to a stream
>>>from StringIO import StringIO
>>>stream=StringIO()
>>>engine.write(stream)
>>>
>>># Later, load and run the log with a regular engine
>>>engine = create_engine('sqlite:///:memory:')
>>>log = logengine.load("filename.logsql")
>>>log.run(engine)

"""
import sys
import pickle
import traceback
import sqlalchemy
from sqlalchemy import engine,create_engine,text
from sqlalchemy.engine import url,strategies,default,base
from migrate.versioning import exceptions

def load(*p,**k):
    return SqlLog.load(*p,**k)

class LogDbapiCursor(object):
    """A fake DBAPI cursor"""
    description=None
    rowcount=None
    arraysize=None

    rownumber=None
    connection=None
    messages=None
    lastrowid=None

    def procname(self,procname,parameters=None):
        pass
    def close(self):
        pass
    def execute(self,operation,parameters=None):
        pass
    def execute(self,operation,seq_of_parameters):
        pass
    def fetchone(self):
        return None
    def fetchmany(self,size=None):
        return None
    def fetchall(self):
        return None
    def nextset(self):
        pass
    def setinputsizes(self,sizes):
        pass
    def setoutputsize(self,size,column):
        pass
    def scroll(self,value,mode=None):
        pass
    def next(self):
        pass
    def __iter__(self):
        pass

class LogDbapiConnection(object):
    """A fake DBAPI connection
    We don't want a real connection to the database - we just need access to 
    the dialect as if we had one.
    """
    def close(self):
        pass
    def commit(self):
        pass
    def rollback(self):
        pass
    def cursor(self):
        return LogDbapiCursor()

class SqlLogEntry(object):
    """A single entry in an SqlLog"""
    def __init__(self,statement,parameters=None):
        self.statement=statement
        self.parameters=parameters
        self.traceback=traceback.extract_stack()
    def trace(self):
        return ''.join(traceback.format_list(self.traceback))

    def __eq__(self,value):
        return str(self)==str(value)
    def __str__(self):
        return '\n'.join(map(lambda x: str(x),(self.statement,self.parameters)))

class SqlLog(object):
    """Logs SQL statements to be executed (with consistent behavior) later"""
    def __init__(self):
        self.entries=[]
    
    def add(self,statement,parameters=None):
        """Add a statement and its parameters to the log"""
        entry=SqlLogEntry(statement,parameters)
        self.entries.append(entry)
    
    def __len__(self):
        return len(self.entries)

    def write(self,file):
        """Write this SqlLog to a file"""
        fd=file
        if type(file) is str:
            fd=open(file,'w')

        pickle.dump(self,fd)

        if type(file) is str:
            fd.close()

    @classmethod
    def load(cls,file):
        """Load an SqlLog from a file, which may be analyzed or executed"""
        fd=file
        if type(file) is str:
            fd=open(file)

        self=pickle.load(fd)

        if type(file) is str:
            fd.close()
        return self
    
    @classmethod
    def create(cls,engine):
        """Create a new SqlLog, to which statements will be added"""
        self=cls()
        #TODO: we ought to verify correctness and such based on this engine
        return self
    
    def run(self,url_or_engine,conn_=None):
        """Run the contents of this SqlLog on a database"""
        engine=url_or_engine
        if type(url_or_engine) is str:
            engine=create_engine(url_or_engine)
        conn=conn_
        if conn_ is None:
            conn=engine.contextual_connect()
        try:
            for entry in self.entries:
                try:
                    conn._execute_raw(entry.statement,entry.parameters)
                except sqlalchemy.exceptions.SQLError,e:
                    # SQL error: add the original traceback to the message
                    raise exceptions.LogSqlError(e,entry)
        finally:
            if conn_ is None:
                # connection was made here - clean up
                conn.close()
    
    def __eq__(self,value):
        return str(self)==str(value)
    def __str__(self):
        return '\n'.join(map(lambda x: str(x),self.entries))
    
class LogConnection(engine.Connection):
    def _execute_raw(self,statement,parameters=None,cursor=None,echo=None,context=None,**kwargs):
        """Most engines execute SQL through here - this engine logs it"""
        cursor=None # No cursors in a stream connection; write only

        engine=self.engine
        if echo or engine.echo:
            engine.log(statement)
            engine.log(repr(parameters))
        engine.logsql.add(statement,parameters)
        return cursor

    def close(self):
        """There should be no __connection to close"""
        if hasattr(self,'__connection'):
            self.__connection=None
            del self.__connection
    #def _begin_impl(self):
    #   pass
    #def _commit_impl(self):
    #   pass
    #def _rollback_impl(self):
    #   pass

class LogEngine(base.Engine):
    def __init__(self,*p,**k):
        if len(p)+len(k)>0:
            self.reset(*p,**k)
            
    def _make_url(self,url_):
        try:
            u = url.make_url(url_)
        except sqlalchemy.exceptions.ArgumentError:
            dbms = url_.split('://',1)[0]
            u = url.URL(dbms)
        return u
    def reset(self,name_or_url,**kwargs):
        # Pasted from sqlalchemy.engine.strategies.PlainEngineStrategy:create
        #u = url.make_url(name_or_url)
        u = self._make_url(name_or_url)
        module = u.get_module()

        args = u.query.copy()
        args.update(kwargs)
        dialect = module.dialect(**args)

        poolargs = {}
        for key in (('echo_pool', 'echo'), ('pool_size', 'pool_size'), ('max_overflow', 'max_overflow'), ('poolclass', 'poolclass'), ('pool_timeout','timeout'), ('pool', 'pool')):
            if kwargs.has_key(key[0]):
                poolargs[key[1]] = kwargs[key[0]]
        poolclass = getattr(module, 'poolclass', None)
        if poolclass is not None:
            poolargs.setdefault('poolclass', poolclass)
        poolargs['use_threadlocal'] = False
        provider = default.PoolConnectionProvider(dialect, u, **poolargs)

        #return LogEngine(provider, dialect, **args)
        #super(LogConnection,self).__init__(*p,**k)
        super(LogEngine,self).__init__(provider,dialect,**args)
        self.logsql=SqlLog.create(self)
        self.drivername = u.drivername

    def connect(self,**kwargs):
        return LogConnection(self,**kwargs)
    def contextual_connect(self,close_with_result=False,**kwargs):
        return self.connect(close_with_result=close_with_result,**kwargs)
    
    def write(self,*p,**k):
        """Write the sql log to a file"""
        return self.logsql.write(*p,**k)
    
    def raw_connection(self,*p,**k):
        return LogDbapiConnection()


class LogEngineStrategy(strategies.EngineStrategy):
    def __init__(self):
        super(LogEngineStrategy,self).__init__('logsql')
    def create(self,name_or_url,**kwargs):
        # Content moved to engine.reset()
        ret = LogEngine()
        if name_or_url is not None:
            ret.reset(name_or_url,**kwargs)
        return ret
LogEngineStrategy()
