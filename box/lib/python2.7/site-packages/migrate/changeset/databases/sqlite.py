from migrate.changeset import ansisql,util,constraint
from sqlalchemy.databases import sqlite
import sqlalchemy
from migrate.changeset import exceptions

class SQLiteColumnGenerator(sqlite.SQLiteSchemaGenerator,ansisql.ANSIColumnGenerator):
    pass
class SQLiteColumnDropper(ansisql.ANSIColumnDropper):
    def visit_column(self,column):
        raise exceptions.NotSupportedError("SQLite does not support "
            "DROP COLUMN; see http://www.sqlite.org/lang_altertable.html")
class SQLiteSchemaChanger(ansisql.ANSISchemaChanger):
    def _not_supported(self,op):
        raise exceptions.NotSupportedError("SQLite does not support "
            "%s; see http://www.sqlite.org/lang_altertable.html"%op)
    def _visit_column_nullable(self,table_name,col_name,delta):
        return self._not_supported('ALTER TABLE')
    def _visit_column_default(self,table_name,col_name,delta):
        return self._not_supported('ALTER TABLE')
    def _visit_column_type(self,table_name,col_name,delta):
        return self._not_supported('ALTER TABLE')
    def _visit_column_name(self,table_name,col_name,delta):
        return self._not_supported('ALTER TABLE')
    def visit_index(self,param):
        self._not_supported('ALTER INDEX')
class SQLiteConstraintGenerator(ansisql.ANSIConstraintGenerator):
    def visit_migrate_primary_key_constraint(self,constraint):
        tmpl = "CREATE UNIQUE INDEX %s ON %s ( %s )"
        cols = ','.join([c.name for c in constraint.columns])
        tname = constraint.table.name
        name = constraint.name
        msg = tmpl%(name,tname,cols)
        self.append(msg)
        self.execute()
class SQLiteConstraintDropper(object):
    def visit_migrate_primary_key_constraint(self,constraint):
        tmpl = "DROP INDEX %s "
        name = constraint.name
        msg = tmpl%(name)
        self.append(msg)
        self.execute()

class SQLiteDialectChangeset(object):
    columngenerator = SQLiteColumnGenerator
    columndropper = SQLiteColumnDropper
    schemachanger = SQLiteSchemaChanger

def _patch():
    util.prepend_base(sqlite.SQLiteDialect,SQLiteDialectChangeset)
    sqlite.SQLiteSchemaGenerator.__bases__ += (SQLiteConstraintGenerator,)
    util.prepend_base(sqlite.SQLiteSchemaDropper,SQLiteConstraintDropper)
