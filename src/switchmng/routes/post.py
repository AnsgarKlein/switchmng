from . import *

@restbp.route('/switch_models', methods = ['POST'])
def post_switch_model():
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

    # Add to database
    try:
        sm = db.add_switch_model(**req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data': sm.jsonify() }, 201

@restbp.route('/switches', methods = ['POST'])
def post_switch():
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

    # Add to database
    try:
        sw = db.add_switch(**req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data': sw.jsonify() }, 201

@restbp.route('/port_types', methods = ['POST'])
def post_port_types():
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

    # Add to database
    try:
        pt = db.add_port_type(**req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data': pt.jsonify() }, 201

@restbp.route('/vlans', methods = ['POST'])
def post_vlans():
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

    # Add to database
    try:
        vl = db.add_vlan(**req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'result': True,
             'data': vl.jsonify() }, 201

