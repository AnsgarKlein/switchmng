from . import *

def _configure_errors(app):
    @app.errorhandler(400)
    def ierror_400(error):
        return error_400()

    @app.errorhandler(401)
    def ierror_401(error):
        return error_401()

    @app.errorhandler(403)
    def ierror_403(error):
        return error_403()

    @app.errorhandler(404)
    def ierror_404(error):
        return error_404()

    @app.errorhandler(405)
    def ierror_405(error):
        return error_405()

    @app.errorhandler(406)
    def ierror_406(error):
        return error_406()

    def ierror_407(error):
        return error_407()

    @app.errorhandler(408)
    def ierror_408(error):
        return error_408()

    @app.errorhandler(409)
    def ierror_409(error):
        return error_409()

    @app.errorhandler(410)
    def ierror_410(error):
        return error_410()

    @app.errorhandler(411)
    def ierror_411(error):
        return error_411()

    @app.errorhandler(412)
    def ierror_412(error):
        return error_412()

    @app.errorhandler(413)
    def ierror_413(error):
        return error_413()

    @app.errorhandler(414)
    def ierror_414(error):
        return error_414()

    @app.errorhandler(415)
    def ierror_415(error):
        return error_415()

    @app.errorhandler(416)
    def ierror_416(error):
        return error_416()

    @app.errorhandler(417)
    def ierror_417(error):
        return error_417()

    @app.errorhandler(418)
    def ierror_418(error):
        return error_418()

    def ierror_421(error):
        return error_412()

    def ierror_425(error):
        return error_425()

    def ierror_426(error):
        return error_425()

    @app.errorhandler(428)
    def ierror_428(error):
        return error_428()

    @app.errorhandler(429)
    def ierror_429(error):
        return error_429()

    @app.errorhandler(431)
    def ierror_431(error):
        return error_431()

    @app.errorhandler(451)
    def ierror_451(error):
        return error_451()

    @app.errorhandler(500)
    def ierror_500(error):
        return error_500()

    @app.errorhandler(Exception)
    def ierror_unknown(error):
        return _error(code = 500, message = 'Unknown Internal Server Error')

def error_400(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Bad Request'
    return _error(code = 400, message = message)

def error_401(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Unauthorized'
    return _error(code = 401, message = message)

def error_403(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Forbidden'
    return _error(code = 403, message = message)

def error_404(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Not Found'
    return _error(code = 404, message = message)

def error_405(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Method Not Allowed'
    return _error(code = 405, message = message)

def error_406(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Not Acceptable'
    return _error(code = 406, message = message)

def error_407(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Proxy Authentication Required'
    return _error(code = 407, message = message)

def error_408(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Request Timeout'
    return _error(code = 408, message = message)

def error_409(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Conflict'
    return _error(code = 409, message = message)

def error_410(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Gone'
    return _error(code = 410, message = message)

def error_411(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Length Required'
    return _error(code = 411, message = message)

def error_412(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Precondition Failed'
    return _error(code = 412, message = message)

def error_413(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Payload Too Large'
    return _error(code = 413, message = message)

def error_414(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'URI Too Long'
    return _error(code = 414, message = message)

def error_415(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Unsupported Media Type'
    return _error(code = 415, message = message)

def error_416(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Range Not Satisfiable'
    return _error(code = 416, message = message)

def error_417(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Expectation Failed'
    return _error(code = 417, message = message)

def error_418(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = "I'm a teapot"
    return _error(code = 418, message = message)

def error_421(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Misdirected Request'
    return _error(code = 421, message = message)

def error_425(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Too Early'
    return _error(code = 425, message = message)

def error_426(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Upgrade Required'
    return _error(code = 426, message = message)

def error_428(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Precondition Required'
    return _error(code = 428, message = message)

def error_429(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Too Many Requests'
    return _error(code = 429, message = message)

def error_431(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Request Header Fields Too Large'
    return _error(code = 431, message = message)

def error_451(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Unavailable For Legal Reasons'
    return _error(code = 451, message = message)

def error_500(message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Internal Server Error'
    return _error(code = 500, message = message)

def _error(code = 500, message = None):
    if not isinstance(message, str) or len(message) < 1:
        message = 'Unknown Internal Server Error'
    if not isinstance(code, int):
        code = 500

    return { 'data': None,
             'result': False,
             'error': code,
             'message': message }, code

