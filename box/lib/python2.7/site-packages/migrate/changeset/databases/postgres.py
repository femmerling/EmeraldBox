from migrate.changeset import ansisql,util
from sqlalchemy.databases import postgres
import sqlalchemy

class PGColumnGenerator(postgres.PGSchemaGenerator,ansisql.ANSIColumnGenerator):
    pass
class PGColumnDropper(ansisql.ANSIColumnDropper):
    pass
class PGSchemaChanger(ansisql.ANSISchemaChanger):
    pass
class PGConstraintGenerator(ansisql.ANSIConstraintGenerator):
    pass
class PGConstraintDropper(ansisql.ANSIConstraintDropper):
    pass

class PGDialectChangeset(object):
    columngenerator = PGColumnGenerator
    columndropper = PGColumnDropper
    schemachanger = PGSchemaChanger

def _patch():
    util.prepend_base(postgres.PGDialect,PGDialectChangeset)
    postgres.PGSchemaGenerator.__bases__ += (PGConstraintGenerator,)
    postgres.PGSchemaDropper.__bases__ += (PGConstraintDropper,)
