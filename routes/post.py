from . import *

@app.route('/switch_models', methods = ['POST'])
def post_switch_model():
    # Check request
    if request.content_type != 'application/json':
        return error_415('Expected content type to be application/json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Add to database
    try:
        db = DatabaseConnection()
        sm = db.add_switch_model(**req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data': sm.jsonify() }, 201

@app.route('/switches', methods = ['POST'])
def post_switch():
    # Check request
    if request.content_type != 'application/json':
        return error_415('Expected content type to be application/json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Add to database
    try:
        db = DatabaseConnection()
        sw = db.add_switch(**req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data': sw.jsonify() }, 201

@app.route('/port_types', methods = ['POST'])
def post_port_types():
    # Check request
    if request.content_type != 'application/json':
        return error_415('Expected content type to be application/json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Add to database
    try:
        db = DatabaseConnection()
        pt = db.add_port_type(**req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data': pt.jsonify() }, 201

@app.route('/vlans', methods = ['POST'])
def post_vlans():
    # Check request
    if request.content_type != 'application/json':
        return error_415('Expected content type to be application/json')
    try:
        req = request.json
        if type(req) is not dict:
            raise BaseException()
    except:
        return error_400('Request is not a valid json object')

    # Add to database
    try:
        db = DatabaseConnection()
        vl = db.add_vlan(**req)
    except BaseException as e:
        return error_400(str(e))

    return { 'result': True,
             'data': vl.jsonify() }, 201

