from flask import Blueprint
from flask import Flask
from flask import abort
from flask import request

from switchmng import database

restbp = Blueprint('REST API', __name__)

from .errors import *
from .delete import *
from .errors import *
from .get    import *
from .patch  import *
from .post   import *
from .put    import *

def create_app(database):

    app = Flask('switchmng')
    app.url_map.strict_slashes = False
    app.config['SWITCHMNG_DB_CONNECTION'] = database
    app.register_blueprint(restbp)

    return app
