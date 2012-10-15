
from sqlalchemy.util import OrderedDict

#databases = ('sqlite','postgres','mysql','oracle','mssql','firebird')
databases = ('sqlite','postgres','mysql','oracle','mssql')

# Map operation names to function names
operations = OrderedDict()
operations['upgrade'] = 'upgrade'
operations['downgrade'] = 'downgrade'
