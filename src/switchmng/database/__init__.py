from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from switchmng.schema import *

dbtype = 'sqlite'
dbstr = 'example.db'

# Initialize sqlalchemy scoped sessions for multi thread requests
print('Initializing session registry...')

# Initialize db engine
if dbtype != 'sqlite':
    raise NotImplementedError('Databases other than sqlite are not yet supported')
engine = create_engine('sqlite:///' +dbstr)
Base.metadata.create_all(engine)
Base.metadata.bin = engine

# Initialize scoped sessions to support multi thread access to database
sessionm = sessionmaker(bind = engine)
Session = scoped_session(sessionm)

from .query import *
from .delete import *
from .modify import *
from .set import *
from .add import *
