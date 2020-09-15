from flask import Blueprint
from flask import abort
from flask import request

from switchmng import database

restbp = Blueprint('REST API', __name__)

from . import delete
from . import errors
from . import get
from . import patch
from . import post
from . import put
