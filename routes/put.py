from . import *

@app.route('/switch_models/<string:resource_id>', methods = ['PUT'])
def put_switch_model(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected content type to be application/json')
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

@app.route('/switches/<string:resource_id>', methods = ['PUT'])
def put_switch(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected content type to be application/json')
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

@app.route('/port_types/<string:resource_id>', methods = ['PUT'])
def put_port_type(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected content type to be application/json')
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

@app.route('/vlans/<int:resource_id>', methods = ['PUT'])
def put_vlan(resource_id):
    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected content type to be application/json')
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

