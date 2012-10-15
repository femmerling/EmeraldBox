from script import *

class SqlFile(ScriptFile):
    """A file containing plain SQL statements."""
    def __init__(self,path):
        super(SqlFile,self).__init__(path)
        file = open(path)
        self.text = file.read()
        file.close()

    def run(self,engine,step):
        text = self.text
        # Don't rely on SA's autocommit here
        # (SA uses .startswith to check if a commit is needed. What if script
        # starts with a comment?)
        conn = engine.connect()
        try:
            trans = conn.begin()
            try:
                conn.execute(text)
                # Success
                trans.commit()
            except:
                trans.rollback()
                raise
        finally:
            conn.close()
