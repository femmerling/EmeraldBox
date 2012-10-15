from migrate.changeset import ansisql,util,exceptions
from sqlalchemy.databases import mysql
import sqlalchemy

class MySQLColumnGenerator(mysql.MySQLSchemaGenerator,ansisql.ANSIColumnGenerator):
    pass
class MySQLColumnDropper(ansisql.ANSIColumnDropper):
    pass
class MySQLSchemaChanger(mysql.MySQLSchemaGenerator,ansisql.ANSISchemaChanger):
    def visit_column(self,delta):
        keys = delta.keys()
        if 'type' in keys or 'nullable' in keys or 'name' in keys:
            self._run_subvisit(delta,self._visit_column_change)
        if 'default' in keys:
            # Column name might have changed above
            col_name = delta.get('name',delta.current_name)
            self._run_subvisit(delta,self._visit_column_default,col_name=col_name)
    def _visit_column_change(self,table_name,col_name,delta):
        if not hasattr(delta,'result_column'):
            # Mysql needs the whole column definition, not just a lone name/type
            raise exceptions.NotSupportedError(
                "A column object is required to do this")
                
        column = delta.result_column
        colspec = self.get_column_specification(column)
        self.start_alter_table(table_name)
        self.append("CHANGE COLUMN ")
        self.append(col_name)
        self.append(' ')
        self.append(colspec)
    def visit_index(self,param):
        # If MySQL can do this, I can't find how
        raise exceptions.NotSupportedError("MySQL cannot rename indexes")
class MySQLConstraintGenerator(ansisql.ANSIConstraintGenerator):
    pass
class MySQLConstraintDropper(ansisql.ANSIConstraintDropper):
    #def visit_constraint(self,constraint):
    #    if isinstance(constraint,sqlalchemy.schema.PrimaryKeyConstraint):
    #        return self._visit_constraint_pk(constraint)
    #    elif isinstance(constraint,sqlalchemy.schema.ForeignKeyConstraint):
    #        return self._visit_constraint_fk(constraint)
    #    return super(MySQLConstraintDropper,self).visit_constraint(constraint)
    def visit_migrate_primary_key_constraint(self,constraint):
        self.start_alter_table(constraint)
        self.append("DROP PRIMARY KEY")
        self.execute()

    def visit_migrate_foreign_key_constraint(self,constraint):
        self.start_alter_table(constraint)
        self.append("DROP FOREIGN KEY ")
        self.append(constraint.name)
        self.execute()

class MySQLDialectChangeset(object):
    columngenerator = MySQLColumnGenerator
    columndropper = MySQLColumnDropper
    schemachanger = MySQLSchemaChanger

def _patch():
    util.prepend_base(mysql.MySQLDialect,MySQLDialectChangeset)
    mysql.MySQLSchemaGenerator.__bases__ += (MySQLConstraintGenerator,)
    mysql.MySQLSchemaDropper.__bases__ += (MySQLConstraintDropper,)
