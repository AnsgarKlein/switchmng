from .blueprint import restbp

@restbp.errorhandler(400)
def ierror_400(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 400"""
    return error_400()

@restbp.errorhandler(401)
def ierror_401(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 401"""
    return error_401()

@restbp.errorhandler(403)
def ierror_403(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 403"""
    return error_403()

@restbp.errorhandler(404)
def ierror_404(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 404"""
    return error_404()

@restbp.errorhandler(405)
def ierror_405(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 405"""
    return error_405()

@restbp.errorhandler(406)
def ierror_406(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 406"""
    return error_406()

@restbp.errorhandler(408)
def ierror_408(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 408"""
    return error_408()

@restbp.errorhandler(409)
def ierror_409(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 409"""
    return error_409()

@restbp.errorhandler(410)
def ierror_410(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 410"""
    return error_410()

@restbp.errorhandler(411)
def ierror_411(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 411"""
    return error_411()

@restbp.errorhandler(412)
def ierror_412(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 412"""
    return error_412()

@restbp.errorhandler(413)
def ierror_413(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 413"""
    return error_413()

@restbp.errorhandler(414)
def ierror_414(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 414"""
    return error_414()

@restbp.errorhandler(415)
def ierror_415(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 415"""
    return error_415()

@restbp.errorhandler(416)
def ierror_416(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 416"""
    return error_416()

@restbp.errorhandler(417)
def ierror_417(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 417"""
    return error_417()

@restbp.errorhandler(418)
def ierror_418(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 418"""
    return error_418()

@restbp.errorhandler(428)
def ierror_428(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 428"""
    return error_428()

@restbp.errorhandler(429)
def ierror_429(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 429"""
    return error_429()

@restbp.errorhandler(431)
def ierror_431(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 431"""
    return error_431()

@restbp.errorhandler(451)
def ierror_451(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 451"""
    return error_451()

@restbp.errorhandler(500)
def ierror_500(error):        #pylint: disable = unused-argument
    """Error handler for HTTP error 500"""
    return error_500()

@restbp.errorhandler(Exception)
def ierror_unknown(error):    #pylint: disable = unused-argument
    """Catch-all error handler"""
    return _error(code = 500, message = 'Unknown Internal Server Error')


def error_400(message = None):
    """JSON error handler for HTTP error 400"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Bad Request'
    return _error(code = 400, message = message)

def error_401(message = None):
    """JSON error handler for HTTP error 401"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Unauthorized'
    return _error(code = 401, message = message)

def error_403(message = None):
    """JSON error handler for HTTP error 403"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Forbidden'
    return _error(code = 403, message = message)

def error_404(message = None):
    """JSON error handler for HTTP error 404"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Not Found'
    return _error(code = 404, message = message)

def error_405(message = None):
    """JSON error handler for HTTP error 405"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Method Not Allowed'
    return _error(code = 405, message = message)

def error_406(message = None):
    """JSON error handler for HTTP error 406"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Not Acceptable'
    return _error(code = 406, message = message)

def error_408(message = None):
    """JSON error handler for HTTP error 408"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Request Timeout'
    return _error(code = 408, message = message)

def error_409(message = None):
    """JSON error handler for HTTP error 409"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Conflict'
    return _error(code = 409, message = message)

def error_410(message = None):
    """JSON error handler for HTTP error 410"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Gone'
    return _error(code = 410, message = message)

def error_411(message = None):
    """JSON error handler for HTTP error 411"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Length Required'
    return _error(code = 411, message = message)

def error_412(message = None):
    """JSON error handler for HTTP error 412"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Precondition Failed'
    return _error(code = 412, message = message)

def error_413(message = None):
    """JSON error handler for HTTP error 413"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Payload Too Large'
    return _error(code = 413, message = message)

def error_414(message = None):
    """JSON error handler for HTTP error 414"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'URI Too Long'
    return _error(code = 414, message = message)

def error_415(message = None):
    """JSON error handler for HTTP error 415"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Unsupported Media Type'
    return _error(code = 415, message = message)

def error_416(message = None):
    """JSON error handler for HTTP error 416"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Range Not Satisfiable'
    return _error(code = 416, message = message)

def error_417(message = None):
    """JSON error handler for HTTP error 417"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Expectation Failed'
    return _error(code = 417, message = message)

def error_418(message = None):
    """JSON error handler for HTTP error 418"""

    if not isinstance(message, str) or len(message) < 1:
        message = "I'm a teapot"
    return _error(code = 418, message = message)

def error_428(message = None):
    """JSON error handler for HTTP error 428"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Precondition Required'
    return _error(code = 428, message = message)

def error_429(message = None):
    """JSON error handler for HTTP error 429"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Too Many Requests'
    return _error(code = 429, message = message)

def error_431(message = None):
    """JSON error handler for HTTP error 431"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Request Header Fields Too Large'
    return _error(code = 431, message = message)

def error_451(message = None):
    """JSON error handler for HTTP error 451"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Unavailable For Legal Reasons'
    return _error(code = 451, message = message)

def error_500(message = None):
    """JSON error handler for HTTP error 500"""

    if not isinstance(message, str) or len(message) < 1:
        message = 'Internal Server Error'
    return _error(code = 500, message = message)

def _error(code = 500, message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Unknown Internal Server Error'
    if not isinstance(code, int):
        code = 500

    return { 'status': code,
             'data': None,
             'message': message }, code
