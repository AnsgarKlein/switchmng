from flask import Blueprint
from flask import abort
from flask import request

from switchmng.database import DatabaseConnection

restbp = Blueprint('REST API', __name__)

from .delete import *
from .errors import *
from .get    import *
from .patch  import *
from .post   import *
from .put    import *
