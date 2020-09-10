import sys

from switchmng import config
from switchmng import database
from switchmng import app

if __name__ == '__main__':
    # Parse command line arguments
    config.parse_arguments(sys.argv[1:])

    # Initialize database
    database.init_db()

    # Run with builtin flask webserver
    app.run(debug = config.DEBUG, host = config.IP, port = config.PORT)

