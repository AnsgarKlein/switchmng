from flask import Flask

from .blueprint import restbp
from .errors import *
from .delete import *
from .errors import *
from .get    import *
from .patch  import *
from .post   import *
from .put    import *

def create_app(database_connection):

    app = Flask('switchmng')
    app.url_map.strict_slashes = False
    app.config['SWITCHMNG_DB_CONNECTION'] = database_connection
    app.register_blueprint(restbp)

    return app
