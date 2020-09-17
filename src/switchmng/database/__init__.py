from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from switchmng.schema import *

from .helper import *

from .query  import *
from .delete import *
from .modify import *
from .set    import *
from .add    import *

class DatabaseConnection():
    def __init__(self, dbtype, dbstr, base):
        # Initialize db engine
        if dbtype == 'sqlite':
            if dbstr == '':
                # Warn when creating an in-memory sqlite database
                print('WARNING: Using an in-memory sqlite database!\n'
                    + '         Changes will not be persistent!')

                dbstr = 'sqlite://'
            else:
                dbstr = 'sqlite:///' + dbstr
        else:
            raise NotImplementedError('Databases other than sqlite are not yet supported')

        self.engine = create_engine(dbstr, echo = False)

        self.base = base
        self.base.metadata.create_all(self.engine)
        self.base.metadata.bin = self.engine

        # Initialize scoped sessions to support multi thread access to database
        self.sessionm = sessionmaker(bind = self.engine)
        self.Session = scoped_session(self.sessionm)

