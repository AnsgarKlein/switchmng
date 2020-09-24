from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng.routes import create_app

def app(*args, **kwargs):
    """
    Entry point for wsgi server like `gunicorn` serving this
    application.

    Parse all command line arguments, initialize application then
    start this application.
    """

    help_str = 'Possible parameters:\n'\
             + '  config=FILE    Use FILE for configuration file'

    # Parse gunicorn parameters, convert them to normal sys.argv style
    # parameters and pass them to parsing function.
    params = []
    for k in kwargs:
        if k == 'config':
            params.append('--config')
            params.append(kwargs[k])
        else:
            print('Unknown parameter "{}"\n\n{}\n'.format(k, help_str))
            return None

    # Parse given arguments
    config.parse_arguments(params)

    # Initialize the database
    db = DatabaseConnection(config.DB_TYPE, config.DB_PATH, config.DB_VERBOSE, Base)

    # Return wsgi app
    app = create_app(db)
    return app
