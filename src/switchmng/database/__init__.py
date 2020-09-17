from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import StaticPool

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
                print('##################################################\n'
                    + '#                    WARNING                     #\n'
                    + '#      Using an in-memory sqlite database!       #\n'
                    + '#        Changes will not be persistent!         #\n'
                    + '##################################################')

                # Make sure that access to in-memory sqlite database only
                # happens from one single connection (StaticPool)
                self.engine = create_engine('sqlite://',
                                            echo = False,
                                            connect_args = {
                                                "check_same_thread": False },
                                            poolclass = StaticPool)
            else:
                dbstr = 'sqlite:///' + dbstr
                self.engine = create_engine(dbstr, echo = False)
        else:
            raise NotImplementedError('Databases other than sqlite are not yet supported')

        self.base = base
        self.base.metadata.create_all(self.engine)
        self.base.metadata.bin = self.engine

        # Initialize scoped sessions to support multi thread access to database
        self.sessionm = sessionmaker(bind = self.engine)
        self.Session = scoped_session(self.sessionm)

