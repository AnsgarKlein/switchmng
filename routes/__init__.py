from flask import Flask
from flask import abort
from flask import request

app = Flask('REST API')
app.url_map.strict_slashes = False

from database import DatabaseConnection

from .errors import *
from .get    import *
from .patch  import *
from .post   import *
from .put    import *
