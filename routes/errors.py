from . import *

@app.errorhandler(400)
def error_400(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Bad Request'
    return _error(code = 400, message = message)

@app.errorhandler(401)
def error_401(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Unauthorized'
    return _error(code = 401, message = message)

@app.errorhandler(403)
def error_403(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Forbidden'
    return _error(code = 403, message = message)

@app.errorhandler(404)
def error_404(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Not Found'
    return _error(code = 404, message = message)

@app.errorhandler(405)
def error_405(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Method Not Allowed'
    return _error(code = 405, message = message)

@app.errorhandler(406)
def error_406(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Not Acceptable'
    return _error(code = 406, message = message)

def error_407(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Proxy Authentication Required'
    return _error(code = 407, message = message)

@app.errorhandler(408)
def error_408(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Request Timeout'
    return _error(code = 408, message = message)

@app.errorhandler(409)
def error_409(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Conflict'
    return _error(code = 409, message = message)

@app.errorhandler(410)
def error_410(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Gone'
    return _error(code = 410, message = message)

@app.errorhandler(411)
def error_411(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Length Required'
    return _error(code = 411, message = message)

@app.errorhandler(412)
def error_412(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Precondition Failed'
    return _error(code = 412, message = message)

@app.errorhandler(413)
def error_413(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Payload Too Large'
    return _error(code = 413, message = message)

@app.errorhandler(414)
def error_414(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'URI Too Long'
    return _error(code = 414, message = message)

@app.errorhandler(415)
def error_415(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Unsupported Media Type'
    return _error(code = 415, message = message)

@app.errorhandler(416)
def error_416(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Range Not Satisfiable'
    return _error(code = 416, message = message)

@app.errorhandler(417)
def error_417(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Expectation Failed'
    return _error(code = 417, message = message)

@app.errorhandler(418)
def error_418(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = "I'm a teapot"
    return _error(code = 418, message = message)

def error_421(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Misdirected Request'
    return _error(code = 421, message = message)

def error_425(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Too Early'
    return _error(code = 425, message = message)

def error_426(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Upgrade Required'
    return _error(code = 426, message = message)

@app.errorhandler(428)
def error_428(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Precondition Required'
    return _error(code = 428, message = message)

@app.errorhandler(429)
def error_429(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Too Many Requests'
    return _error(code = 429, message = message)

@app.errorhandler(431)
def error_431(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Request Header Fields Too Large'
    return _error(code = 431, message = message)

@app.errorhandler(451)
def error_451(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Unavailable For Legal Reasons'
    return _error(code = 451, message = message)

@app.errorhandler(500)
def error_500(error = None, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Internal Server Error'
    return _error(code = 500, message = message)


@app.errorhandler(Exception)
def error_unknown(error):
    return _error(code = 500, message = 'Unknown Internal Server Error')


def _error(code = 500, message = None):
    if type(message) is not str or len(message) < 1:
        message = 'Unknown Internal Server Error'
    if type(code) is not int:
        code = 500

    return { 'data': None,
             'result': False,
             'error': code,
             'message': message }, code
