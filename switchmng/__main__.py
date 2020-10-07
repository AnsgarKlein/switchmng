import sys

from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng import routes

def main() -> int:    #pragma: no cover
    """
    Run `switchmng` directly.

    Parse all command line arguments, decide which mode to run in,
    then start.
    """

    # Parse command line arguments
    config.parse_arguments(sys.argv[1:])

    # Initialize database
    db = DatabaseConnection(config.DB_TYPE, config.DB_PATH, config.DB_VERBOSE, Base)

    # Choose main function depending on mode
    if config.MODE == 'webserver':
        return webserver_main(db)

    if config.MODE == 'dump':
        raise NotImplementedError('dump is not yet implemented!')

    return 1

def webserver_main(db)-> int:    #pragma: no cover
    """Main function when running in webserver mode"""

    # Run with builtin flask webserver
    app = routes.create_app(db)
    app.run(debug = config.DEBUG, host = config.IP, port = config.PORT)
    return 0

if __name__ == '__main__':
    sys.exit(main())
