from . import *

@app.errorhandler(404)
def error404(error):
    return { 'data': None,
             'result': False,
             'error': 404,
             'message': 'Not found' }, 404

