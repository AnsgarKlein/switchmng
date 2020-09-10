from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from switchmng import config

from .query import *
from .delete import *
from .modify import *
from .set import *
from .add import *

def init_db():
    # Initialize db engine
    if config.DB_TYPE == 'sqlite':
        if config.DB_PATH == '':
            # Warn when creating an in-memory sqlite database
            print('WARNING: Using an in-memory sqlite database!\n'
                + '         Changes will not be persistent!')

            dbstr = 'sqlite://'
        else:
            dbstr = 'sqlite:///' + config.DB_PATH
    else:
        raise NotImplementedError('Databases other than sqlite are not yet supported')

    engine = create_engine(dbstr, echo = False)

    Base.metadata.create_all(engine)
    Base.metadata.bin = engine

    # Initialize scoped sessions to support multi thread access to database
    sessionm = sessionmaker(bind = engine)

    global Session
    Session = scoped_session(sessionm)

