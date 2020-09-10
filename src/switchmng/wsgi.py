from switchmng import config
from switchmng import database
from switchmng import app as a

import sys

# Entry point for gunicorn
def app(*args, **kwargs):
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
    database.init_db()

    # Return wsgi app
    return a

