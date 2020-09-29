import sys

from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng import routes

def main():
    """
    Run `switchmng` module directly.

    Parse all command line arguments, initialize application then
    start this application.
    """

    # Parse command line arguments
    config.parse_arguments(sys.argv[1:])

    # Initialize database
    db = DatabaseConnection(config.DB_TYPE, config.DB_PATH, config.DB_VERBOSE, Base)

    if config.MODE == 'webserver':
        # Run with builtin flask webserver
        app = routes.create_app(db)
        app.run(debug = config.DEBUG, host = config.IP, port = config.PORT)
    elif config.MODE == 'dump':
        raise NotImplementedError('dump is not yet implemented!')

if __name__ == '__main__':
    main()
