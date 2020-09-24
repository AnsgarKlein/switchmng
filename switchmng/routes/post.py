from flask import current_app
from flask import abort
from flask import request

from switchmng import database
from .blueprint import restbp
from .errors import *

@restbp.route('/switch_models', methods = ['POST'])
def post_switch_model():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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

@restbp.route('/switch_models/<string:switch_model_resource_id>/ports', methods = ['POST'])
def post_port_model(switch_model_resource_id):
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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
        pm = database.add_port_model(session, switch_model_resource_id, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': pm.jsonify() }, 201

@restbp.route('/switches', methods = ['POST'])
def post_switch():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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

@restbp.route('/network_protocols', methods = ['POST'])
def post_network_protocol():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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
        np = database.add_network_protocol(session, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': np.jsonify() }, 201

@restbp.route('/connectors', methods = ['POST'])
def post_connector():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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
        cn = database.add_connector(session, **req)
    except BaseException as e:
        return error_400(message = str(e))

    return { 'status': 201,
             'data': cn.jsonify() }, 201

@restbp.route('/vlans', methods = ['POST'])
def post_vlan():
    session = current_app.config['SWITCHMNG_DB_CONNECTION'].Session()

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
