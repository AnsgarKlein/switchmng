from flask import Flask
from flask import abort
from flask import request

from switchmng import database
import switchmng.database

from .errors import *

from .delete import _configure_delete
from .errors import _configure_errors
from .get    import _configure_get
from .patch  import _configure_patch
from .post   import _configure_post
from .put    import _configure_put

def create_app(database):
    app = Flask('switchmng')
    app.url_map.strict_slashes = False
    app.config['SWITCHMNG_DB_CONNECTION'] = database

    _configure_delete(app)
    _configure_errors(app)
    _configure_get(app)
    _configure_patch(app)
    _configure_post(app)
    _configure_put(app)

    return app
