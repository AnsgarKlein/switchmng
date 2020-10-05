from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import StaticPool

from .query  import *
from .delete import *
from .modify import *
from .set    import *
from .add    import *

class DatabaseConnection():
    def __init__(self, db_type: str, db_str: str, db_verbose: bool, base):
        # Initialize db engine
        if db_type == 'sqlite':
            if db_str == '':
                # Warn when creating an in-memory sqlite database
                print('##################################################\n'
                    + '#                    WARNING                     #\n'
                    + '#      Using an in-memory sqlite database!       #\n'
                    + '#        Changes will not be persistent!         #\n'
                    + '##################################################')

                # Make sure that access to in-memory sqlite database only
                # happens from one single connection (StaticPool)
                self.engine = create_engine('sqlite://',
                                            echo = db_verbose,
                                            connect_args = {
                                                "check_same_thread": False },
                                            poolclass = StaticPool)
            else:
                db_str = 'sqlite:///' + db_str
                self.engine = create_engine(db_str, echo = db_verbose)
        else:
            raise NotImplementedError('Databases other than sqlite are not yet supported')

        self.base = base
        self.base.metadata.create_all(self.engine)
        self.base.metadata.bin = self.engine

        # Initialize scoped sessions to support multi thread access to database
        self.sessionm = sessionmaker(bind = self.engine)
        self.Session = scoped_session(self.sessionm)
