from . import *

@app.route('/switch_models/<string:resource_id>', methods = ['PATCH'])
def patch_switch_model(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415('Expected content type to be application/merge-patch+json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        sm = db.modify_switch_model(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data:': sm.jsonify() }, 200

@app.route('/switches/<string:resource_id>', methods = ['PATCH'])
def patch_switch(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415('Expected content type to be application/merge-patch+json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        sw = db.modify_switch(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data:': sw.jsonify() }, 200

@app.route('/port_types/<string:resource_id>', methods = ['PATCH'])
def patch_port_type(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415('Expected content type to be application/merge-patch+json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        pt = db.modify_port_type(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data:': pt.jsonify() }, 200

@app.route('/vlans/<int:resource_id>', methods = ['PATCH'])
def patch_vlan(resource_id):
    # Check request
    if request.content_type != 'application/merge-patch+json':
        return error_415('Expected content type to be application/merge-patch+json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Modify in database
    try:
        db = DatabaseConnection()
        vl = db.modify_vlan(resource_id = resource_id, **req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data:': vl.jsonify() }, 200

