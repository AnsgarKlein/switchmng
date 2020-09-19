from flask import current_app

from . import *

@restbp.route('/switch_models', methods = ['POST'])
def post_switch_model():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Add to database
    try:
        sm = database.add_switch_model(session, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': sm.jsonify() }, 201

@restbp.route('/switches', methods = ['POST'])
def post_switch():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Add to database
    try:
        sw = database.add_switch(session, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': sw.jsonify() }, 201

@restbp.route('/port_types', methods = ['POST'])
def post_port_types():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Add to database
    try:
        pt = database.add_port_type(session, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': pt.jsonify() }, 201

@restbp.route('/vlans', methods = ['POST'])
def post_vlans():
    db = current_app.config['SWITCHMNG_DB_CONNECTION']
    session = db.Session()

    # Check request
    if request.content_type != 'application/json':
        return error_415(message = 'Expected Content-Type to be application/json')
    if not request.accept_mimetypes.accept_json:
        return error_406(message = 'Content-Type application/json is not accepted by client')
    try:
        req = request.json
        if not isinstance(req, dict):
            raise BaseException()
    except:
        return error_400(message = 'Request is not a valid json object')

    # Add to database
    try:
        vl = database.add_vlan(session, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': vl.jsonify() }, 201

