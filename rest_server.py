from database import DatabaseConnection

from flask import Flask
from flask import abort
from flask import request

app = Flask('REST API')
app.url_map.strict_slashes = False

@app.errorhandler(404)
def error404(error):
    return { 'data': None,
             'result': False,
             'error': 404,
             'message': 'Not found' }, 404

@app.route('/switch_models/<string:resource_id>', methods = ['GET'])
def get_switch_model(resource_id):
    db = DatabaseConnection()
    sm = db.query_switch_model(resource_id)

    if sm is None:
        abort(404)

    return { 'result': True,
             'data': sm.jsonify() }, 200

@app.route('/switches/<string:resource_id>', methods = ['GET'])
def get_switch(resource_id):
    db = DatabaseConnection()
    sw = db.query_switch(resource_id)

    if sw is None:
        abort(404)

    return { 'result': True,
             'data': sw.jsonify() }, 200

@app.route('/port_types/<string:resource_id>', methods = ['GET'])
def get_port_type(resource_id):
    db = DatabaseConnection()
    pt = db.query_port_type(resource_id)

    if pt is None:
        abort(404)

    return { 'result': True,
             'data': pt.jsonify() }, 200

@app.route('/vlans/<int:resource_id>', methods = ['GET'])
def get_vlan(resource_id):
    db = DatabaseConnection()
    vl = db.query_vlan(resource_id)

    if vl is None:
        abort(404)

    return { 'result': True,
             'data': vl.jsonify() }, 200

@app.route('/switch_models', methods = ['GET'])
def get_switch_models():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ sm.jsonify() for sm in db.query_switch_models() ] }, 200

@app.route('/switches', methods = ['GET'])
def get_switches():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ sw.jsonify() for sw in db.query_switches() ] }, 200

@app.route('/port_types', methods = ['GET'])
def get_port_types():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ pt.jsonify() for pt in db.query_port_types() ] }, 200

@app.route('/vlans', methods = ['GET'])
def get_vlans():
    db = DatabaseConnection()
    return { 'result': True,
             'data': [ vl.jsonify() for vl in db.query_vlans() ] }, 200

@app.route('/switch_models/<string:resource_id>', methods = ['PATCH'])
def patch_switch_model(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/merge-patch+json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        sm = db.modify_switch_model(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': sm.jsonify() }, 200

@app.route('/switches/<string:resource_id>', methods = ['PATCH'])
def patch_switch(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/merge-patch+json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        sw = db.modify_switch(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': sw.jsonify() }, 200

@app.route('/port_types/<string:resource_id>', methods = ['PATCH'])
def patch_port_type(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/merge-patch+json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        pt = db.modify_port_type(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': pt.jsonify() }, 200

@app.route('/vlans/<int:resource_id>', methods = ['PATCH'])
def patch_vlan(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/merge-patch+json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        vl = db.modify_vlan(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': vl.jsonify() }, 200

@app.route('/switch_models/<string:resource_id>', methods = ['PUT'])
def put_switch_model(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        sm = db.set_switch_model(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': sm.jsonify() }, 200

@app.route('/switches/<string:resource_id>', methods = ['PUT'])
def put_switch(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        sw = db.set_switch(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': sw.jsonify() }, 200

@app.route('/port_types/<string:resource_id>', methods = ['PUT'])
def put_port_type(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        pt = db.set_port_type(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': pt.jsonify() }, 200

@app.route('/vlans/<int:resource_id>', methods = ['PUT'])
def put_vlan(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Modify in database
    try:
        db = DatabaseConnection()
        vl = db.set_vlan(resource_id = resource_id, **req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data:': vl.jsonify() }, 200

@app.route('/switch_models', methods = ['POST'])
def post_switch_model():
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Add to database
    try:
        db = DatabaseConnection()
        sm = db.add_switch_model(**req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data': sm.jsonify() }, 201

@app.route('/switches', methods = ['POST'])
def post_switch():
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Add to database
    try:
        db = DatabaseConnection()
        sw = db.add_switch(**req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data': sw.jsonify() }, 201

@app.route('/port_types', methods = ['POST'])
def post_port_types():
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Add to database
    try:
        db = DatabaseConnection()
        pt = db.add_port_type(**req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data': pt.jsonify() }, 201

@app.route('/vlans', methods = ['POST'])
def post_vlans():
    # Check request
    if request.content_type != 'application/json':
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Expected content type to be application/json' }, 400
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': 'Request is not a valid json object' }, 400

    # Add to database
    try:
        db = DatabaseConnection()
        vl = db.add_vlan(**req)
    except BaseException as e:
        return { 'result': False,
                 'data': None,
                 'error': 400,
                 'message': str(e) }, 400

    return { 'result': True,
             'data': vl.jsonify() }, 201

if __name__ == '__main__':
    app.run(debug= True, host = '127.0.0.1', port = 8000)

