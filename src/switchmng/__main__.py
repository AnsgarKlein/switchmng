import sys

from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng import routes

if __name__ == '__main__':
    # Parse command line arguments
    config.parse_arguments(sys.argv[1:])

    # Initialize database
    db = DatabaseConnection(config.DB_TYPE, config.DB_PATH, Base)

    # Run with builtin flask webserver
    app = routes.create_app(db)
    app.run(debug = config.DEBUG, host = config.IP, port = config.PORT)

