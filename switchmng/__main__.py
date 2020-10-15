import sys

from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng import routes
from switchmng import importer

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

    if config.MODE == 'import':
        return import_main(db)

    if config.MODE == 'dump':
        raise NotImplementedError('dump is not yet implemented!')

    return 1

def webserver_main(db)-> int:    #pragma: no cover
    """Main function when running in webserver mode"""

    # Run with builtin flask webserver
    app = routes.create_app(db)
    app.run(debug = config.DEBUG, host = config.IP, port = config.PORT)
    return 0

def import_main(db) -> int:    #pragma: no cover
    """Main function when running in import mode"""

    # Initialize database
    db = DatabaseConnection(config.DB_TYPE, config.DB_PATH, config.DB_VERBOSE, Base)

    if not isinstance(config.IMPORT_PATH, str):
        print('No path given', file = sys.stderr)
        return 1

    # Import
    try:
        importer.import_from_path(db, config.IMPORT_PATH, config.IMPORT_TYPE)
    except BaseException as e:
        print(str(e), file = sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
