from . import *

@restbp.route('/switch_models/<string:resource_id>', methods = ['PUT'])
def put_switch_model(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        sm = db.set_switch_model(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': sm.jsonify() }, 200

@restbp.route('/switches/<string:resource_id>', methods = ['PUT'])
def put_switch(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        sw = db.set_switch(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': sw.jsonify() }, 200

@restbp.route('/port_types/<string:resource_id>', methods = ['PUT'])
def put_port_type(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        pt = db.set_port_type(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': pt.jsonify() }, 200

@restbp.route('/vlans/<int:resource_id>', methods = ['PUT'])
def put_vlan(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        vl = db.set_vlan(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data:': vl.jsonify() }, 200
